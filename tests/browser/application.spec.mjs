import { test, expect } from "@playwright/test";
import { spawnSync } from "node:child_process";
import { mkdtemp, readFile, writeFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { fillFields, uploadVerifiedFiles } from "../../scripts/portal-actions.mjs";
import { PortalPage } from "./portal-page.mjs";

const python = process.env.CV_TAILOR_PYTHON || "python";
const helper = resolve("scripts/cvtool.py");
function kit(args, expectedCode = 0) {
  const result = spawnSync(python, [helper, ...args], { encoding: "utf-8" });
  expect(result.status, result.stderr || result.error?.message).toBe(expectedCode);
  return JSON.parse(result.stdout);
}
async function artifacts(directory) {
  const original = JSON.parse(await readFile("examples/document.json", "utf-8"));
  for (const [id, kind] of [["cv", "cv"], ["letter", "cover-letter"], ["certificate", "supporting"]]) {
    const input = join(directory, `${id}.json`);
    await writeFile(input, JSON.stringify({ ...original, kind, title: `Alex Example - ${id}` }));
    kit(["export", "--input", input, "--format", "pdf", "--output", join(directory, id)]);
    kit(["stage", "--workspace", directory, "--file", join(directory, `${id}.pdf`), "--id", id, "--kind", kind]);
  }
  kit(["merge", "--inputs", join(directory, "letter.pdf"), join(directory, "certificate.pdf"), "--output", join(directory, "combined.pdf")]);
  kit(["stage", "--workspace", directory, "--file", join(directory, "combined.pdf"), "--id", "combined", "--kind", "supporting"]);
  return kit(["files", "--workspace", directory, "--documents", "cv", "letter", "certificate", "combined"]);
}
async function record(directory, event) {
  const path = join(directory, "event.json");
  await writeFile(path, JSON.stringify(event));
  return kit(["application", "record", "--workspace", directory, "--event", path]);
}
const verifiedSection = id => ({ type: "section", id, status: "verified", missing_fields: [], unconfirmed_fields: [], portal_saved: false, evidence: "Fixture inputs read back and section validation passed" });
let directory;
test.beforeEach(async () => {
  directory = await mkdtemp(join(process.env.CV_TAILOR_TEST_TEMP || tmpdir(), "cv-tailor-browser-"));
});
test.afterEach(async () => { await rm(directory, { recursive: true, force: true }); });

for (const [mode, arrangement] of [["sap", "separate"], ["sap", "multi"], ["custom", "combined"], ["single", "multi"]]) {
  test(`${mode} portal with ${arrangement} uploads reaches review without submitting`, async ({ page }) => {
    const portal = new PortalPage(page);
    const files = await artifacts(directory);
    const ids = arrangement === "combined" ? ["cv", "combined"] : ["cv", "letter", "certificate"];
    const fields = [{ id: "cv", label: "CV", document_ids: ["cv"], max_files: 1 }];
    if (arrangement === "separate") fields.push({ id: "letter", label: "Cover letter", document_ids: ["letter"], max_files: 1 }, { id: "cert", label: "Certificates", document_ids: ["certificate"], max_files: 2 });
    else fields.push({ id: "other", label: "Other documents", document_ids: arrangement === "combined" ? ["combined"] : ["letter", "certificate"], max_files: arrangement === "combined" ? 1 : 2 });
    kit(["application", "init", "--workspace", directory, "--company", "Example Employer", "--reference", "42", "--url", "https://example.invalid/jobs/42", "--documents", ...ids]);
    await record(directory, { type: "plan", required_sections: ["personal", "experience", "documents"], upload_fields: fields.map(({ label, ...field }) => ({ ...field, required: true, accept: [".pdf", ".docx"], max_bytes: 5_000_000 })) });
    await portal.open(mode, arrangement);
    if (mode === "sap") {
      await record(directory, { type: "block", reason: "login", detail: "Sign in manually in the connected tab" });
      await expect(fillFields(page, [{ label: "Password", type: "text", value: "not-used", confirmed: true }])).rejects.toThrow("manual browser handoff");
      // Simulate the user completing sign-in, not automated credential handling.
      await page.getByRole("button", { name: "Manual sign-in completed" }).click();
      await record(directory, { type: "resume" });
    }
    await portal.personal();
    await record(directory, verifiedSection("personal"));
    if (mode !== "single") await portal.next("Experience");
    await portal.experience();
    await record(directory, verifiedSection("experience"));
    if (mode !== "single") await portal.next("Documents");
    for (const field of fields) {
      await uploadVerifiedFiles(page, field.label, field.document_ids.map(id => files[id]), { accept: [".pdf", ".docx"], maxFiles: field.max_files, maxBytes: 5_000_000 });
      await expect(page.getByLabel(`${field.label} status`, { exact: true })).toContainText("upload complete");
      await record(directory, { type: "upload", field_id: field.id, document_ids: field.document_ids, evidence: "Displayed filenames match the selected records and upload completion is visible" });
    }
    await record(directory, verifiedSection("documents"));
    await expect(page.getByLabel("Optional talent pool", { exact: true })).not.toBeChecked();
    if (mode === "single") await page.getByRole("button", { name: "Review application", exact: true }).click();
    else await portal.next("Review application");
    await expect(page.getByRole("button", { name: "Submit application", exact: true })).toBeVisible();
    await record(directory, { type: "observe", url: page.url(), company: "Example Employer", reference: "42", final_action: "submit_application", validation_errors: [], evidence: "Correct synthetic job; all sections complete; next action submits" });
    expect(kit(["application", "review", "--workspace", directory]).ready).toBe(true);
    expect(await page.evaluate(() => window.fixtureSubmissionCount())).toBe(0);
  });
}

test("manual challenge and reload resume at the correct section", async ({ page }) => {
  const portal = new PortalPage(page);
  await portal.open("custom", "multi", true);
  await expect(page.getByRole("heading", { name: "Manual verification required" })).toBeVisible();
  await page.getByRole("button", { name: "Complete challenge manually" }).click();
  await portal.personal();
  await portal.next("Experience");
  await page.reload();
  await expect(page.getByRole("heading", { name: "Experience", exact: true })).toBeVisible();
  expect(await page.evaluate(() => window.fixtureSubmissionCount())).toBe(0);
});

test("validation, unknown answers, and changed upload files require correction", async ({ page }) => {
  const portal = new PortalPage(page);
  await portal.open("custom", "separate");
  await page.getByRole("button", { name: "Next section" }).click();
  await expect(page.getByRole("alert")).toContainText("Full name");
  await expect(fillFields(page, [{ label: "Full name", type: "text", value: "Guessed", confirmed: false }])).rejects.toThrow("Confirm the answer");
  await expect(page.getByLabel("Full name")).toHaveValue("");
  await portal.personal();
  await portal.next("Experience");
  await portal.experience();
  await portal.next("Documents");
  const files = await artifacts(directory);
  await expect(uploadVerifiedFiles(page, "CV", [files.cv, files.letter])).rejects.toThrow("many files");
  await writeFile(files.cv.absolute_path, "modified");
  await expect(uploadVerifiedFiles(page, "CV", [files.cv])).rejects.toThrow("changed");
  await expect(page.getByLabel("CV status", { exact: true })).toHaveText("");
  expect(await page.evaluate(() => window.fixtureSubmissionCount())).toBe(0);
});

test("ambiguous controls and consent guesses are not clicked", async ({ page }) => {
  await page.setContent('<label>Name<input></label><label>Name<input></label><label><input type="checkbox">Talent pool</label>');
  await expect(fillFields(page, [{ label: "Name", type: "text", value: "Alex", confirmed: true }])).rejects.toThrow("Ambiguous");
  await expect(fillFields(page, [{ label: "Talent pool", type: "checkbox", value: true, confirmed: false }])).rejects.toThrow("Confirm");
  await expect(page.getByLabel("Talent pool")).not.toBeChecked();
  await fillFields(page, [{ label: "Talent pool", type: "checkbox", value: false, confirmed: true }]);
});
