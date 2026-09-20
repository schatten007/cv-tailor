# Custom and unidentified application portals

Start from the actual form and observed controls, whether it is custom-built or
an ATS behind company branding. Do not guess provider behavior.

- Discover field labels, required markers, descriptions, validation messages,
  accepted file types, and progress navigation from current snapshots.
- Handle a single page or multiple sections using the same inspect -> fill ->
  verify -> advance loop. Reinspect after each state change; refs can expire.
- Prefer label/role-based controls. Custom comboboxes may require typing and
  selecting an option, not merely entering text. Inspect frames/popups separately.
- Repeated roles/education need explicit Add/Save operations. Check created rows
  before adding another to avoid duplicates.
- A drop zone and a file chooser may be two interfaces to the same upload. Verify
  the resulting filename and completion status; never equate selecting a file
  with successful upload.
- Wait for visible completion/errors rather than arbitrary sleeps. Retry a
  failing non-submission action at most twice after fresh inspection; then pause
  with the field or widget needing manual attention.
- Ask for unknown mandatory screening answers. Do not silently accept marketing,
  talent-pool retention, declarations, or terms on behalf of the user.
- If a Next control's effect is unclear, stop to inspect. There may be no separate
  review page: once the next action would send the application, create the local
  review summary and leave that control untouched.

For inaccessible widgets or persistent blocking, keep the prepared answers,
documents, and progress available for manual completion. Do not report universal
portal compatibility or a successful application without observed evidence.
