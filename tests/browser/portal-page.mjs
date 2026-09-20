import { expect } from "@playwright/test";
import { fillFields } from "../../scripts/portal-actions.mjs";

// This fixture Page Object exercises the documented observe/fill/advance loop.
// Production portals are inspected live; these selectors are not SAP selectors.
export class PortalPage {
  constructor(page) { this.page = page; }
  async open(mode, uploads, challenge = false) {
    await this.page.goto(`/portal.html?mode=${mode}&uploads=${uploads}&challenge=${challenge ? 1 : 0}`);
  }
  async personal() {
    await fillFields(this.page, [
      { label: "Full name", type: "text", value: "Alex Example", confirmed: true },
      { label: "Email", type: "text", value: "alex@example.invalid", confirmed: true },
      { label: "Contract type", type: "select", value: "Student", confirmed: true },
      { label: "Expected graduation", type: "text", value: "09/2027", confirmed: true },
    ]);
  }
  async experience() {
    await fillFields(this.page, [
      { label: "Employer 1", type: "text", value: "Example Lab", confirmed: true },
      { label: "Job title 1", type: "text", value: "Student assistant", confirmed: true },
    ]);
    await this.page.getByRole("button", { name: "Add experience", exact: true }).click();
    await fillFields(this.page, [
      { label: "Employer 2", type: "text", value: "Example Project", confirmed: true },
      { label: "Job title 2", type: "text", value: "Volunteer developer", confirmed: true },
    ]);
    await expect(this.page.getByLabel("Employer 1", { exact: true })).toHaveValue("Example Lab");
  }
  async next(heading) {
    await this.page.getByRole("button", { name: "Next section", exact: true }).click();
    await expect(this.page.getByRole("heading", { name: heading, exact: true })).toBeVisible();
  }
}
