/**
 * Optional Playwright helpers for an already connected page.
 * No browser launch, navigation, credential handling, or submit operation.
 * Native MCP tools remain the default; use this only when the host supports
 * running local Playwright code against its existing connected page.
 */
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { basename, extname, isAbsolute } from "node:path";

async function uniqueLabel(page, label) {
  if (typeof label !== "string" || !label.trim()) throw new Error("Supply an observed field label");
  const control = page.getByLabel(label, { exact: true });
  if ((await control.count()) !== 1) {
    throw new Error(`Ambiguous or missing field: ${label}; inspect the current section`);
  }
  return control;
}

/** Fill only explicitly confirmed values; never finish a field with Enter. */
export async function fillFields(page, fields) {
  if (!Array.isArray(fields)) throw new Error("Supply a list of confirmed fields");
  for (const field of fields) {
    if (field.confirmed !== true) throw new Error(`Confirm the answer for ${field.label}`);
    if (!["text", "select", "checkbox", "radio"].includes(field.type)) {
      throw new Error("Unsupported widget; use current browser snapshots or manual input");
    }
    if (["checkbox", "radio"].includes(field.type) ? typeof field.value !== "boolean" : typeof field.value !== "string") {
      throw new Error("Field value has the wrong type");
    }
  }
  const verified = [];
  for (const field of fields) {
    const control = await uniqueLabel(page, field.label);
    const info = await control.evaluate((element) => ({
      tag: element.tagName.toLowerCase(),
      type: element.getAttribute("type")?.toLowerCase() || "text",
      autocomplete: element.getAttribute("autocomplete") || "",
    }));
    if (info.type === "password" || /password|one-time-code/i.test(info.autocomplete) || /password|passwort|verification code|captcha|one.time|\botp\b/i.test(field.label)) {
      throw new Error("Credentials and verification require a manual browser handoff");
    }
    if (field.type === "text") {
      if (!["input", "textarea"].includes(info.tag) || ["submit", "button", "file", "hidden", "checkbox", "radio"].includes(info.type)) {
        throw new Error("Target is not an editable text field");
      }
      await control.fill(field.value);
      if ((await control.inputValue()) !== field.value) throw new Error(`Readback failed: ${field.label}`);
    } else if (field.type === "select") {
      if (info.tag !== "select") throw new Error("Custom combobox: inspect and select its actual option");
      await control.selectOption({ label: field.value });
      const selected = await control.evaluate((element) => element.selectedOptions[0]?.textContent?.trim());
      if (selected !== field.value) throw new Error(`Selection readback failed: ${field.label}`);
    } else {
      if (info.tag !== "input" || info.type !== field.type) throw new Error("Target is not the declared checkbox/radio");
      if (field.type === "radio" && !field.value) throw new Error("Select the intended radio option explicitly");
      await control.setChecked(field.value);
      if ((await control.isChecked()) !== field.value) throw new Error(`Choice readback failed: ${field.label}`);
    }
    verified.push(field.label);
  }
  return { verifiedFields: verified, submitted: false };
}

/** Select staged files; the caller still verifies portal upload completion. */
export async function uploadVerifiedFiles(page, label, files, limits = {}) {
  if (!Array.isArray(files) || files.length === 0) throw new Error("Select document records from the manifest");
  const control = await uniqueLabel(page, label);
  const info = await control.evaluate((element) => ({
    tag: element.tagName.toLowerCase(),
    type: element.getAttribute("type"),
    multiple: element.hasAttribute("multiple"),
  }));
  if (info.tag !== "input" || info.type !== "file") throw new Error("Use the actual file input or native MCP file chooser");
  if ((!info.multiple && files.length > 1) || (limits.maxFiles != null && files.length > limits.maxFiles)) {
    throw new Error("This upload field does not accept that many files");
  }
  const paths = [];
  for (const file of files) {
    if (typeof file.absolute_path !== "string" || !isAbsolute(file.absolute_path) || !/^[a-f0-9]{64}$/.test(file.sha256)) {
      throw new Error("Use verified manifest records with absolute paths and SHA-256");
    }
    const extension = extname(file.absolute_path).toLowerCase();
    if (![".pdf", ".docx", ".png", ".jpg", ".jpeg"].includes(extension) || (limits.accept?.length && !limits.accept.includes(extension))) {
      throw new Error("File type is not accepted by this field");
    }
    const bytes = await readFile(file.absolute_path);
    if (bytes.length !== file.size_bytes || createHash("sha256").update(bytes).digest("hex") !== file.sha256) {
      throw new Error("Staged document changed; verify its version before upload");
    }
    if (limits.maxBytes != null && bytes.length > limits.maxBytes) throw new Error("File exceeds the portal limit");
    paths.push(file.absolute_path);
  }
  await control.setInputFiles(paths);
  const selected = await control.evaluate((element) => Array.from(element.files || [], (file) => file.name));
  const expected = paths.map((path) => basename(path));
  if (JSON.stringify(selected) !== JSON.stringify(expected)) throw new Error("File selection did not match the requested documents");
  return { selectedFiles: selected, needsPortalCompletionCheck: true, submitted: false };
}
