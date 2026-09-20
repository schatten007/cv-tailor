# Resumable, review-only application workflow

The browser MCP operates the page. `scripts/cvtool.py application` maintains a
local ledger of verified observations and selected document hashes. It never
opens a portal, clicks a button, or submits an application. Resolve helper paths
relative to the toolkit/installed skill, not the working project.

## Initialize and plan

Stage final documents first, then:

```sh
python scripts/cvtool.py application init --workspace "../career/applications/example-42" --company "Example Employer" --reference "42" --url "https://example.invalid/jobs/42" --documents cv
python scripts/cvtool.py application record --workspace "../career/applications/example-42" --event "../career/events/plan.json"
```

Use the real vacancy URL/reference. Initialization refuses an existing ledger;
reopen it rather than start duplicate applications. `examples/portal-plan.json`
shows a synthetic inventory. Record every observed section, including documents
and required declarations. Later plan events add newly revealed sections; they
cannot silently drop unfinished earlier sections. Update field restrictions from
the current page, not a guessed vendor template. For an undisclosed maximum use
`null`; an empty `accept` list means unknown, not a fabricated restriction.

## Observe -> fill -> verify -> advance

1. Capture a fresh accessibility snapshot. Confirm company/job/account and current
   step. Browser refs are transient and must not be stored as durable selectors.
2. Fill confirmed information using labels/roles or current refs. Ask once for
   related unknown mandatory answers; keep application-specific answers in a
   local answers file. Do not store passwords, cookies, tokens, or MFA codes.
3. Use actual controls for select/combobox/checkbox inputs and repeated entries.
   Inspect newly revealed fields and reread any resume-autofilled data.
4. Check visible validation messages and values. Record each verified section
   using this shape; `portal_saved` means an observed server/draft-save signal,
   not simply that the field was filled:

```json
{"type":"section","id":"personal","status":"verified","missing_fields":[],"unconfirmed_fields":[],"portal_saved":false,"evidence":"Name and email read back correctly; no visible validation errors."}
```

5. Select/upload documents for the actual field. A required single CV field, a
   separate optional letter, a multi-file Other field, and a combined PDF each
   have different `document_ids`/type/count rules. After displayed filenames and
   completion have been verified, record:

```json
{"type":"upload","field_id":"resume","document_ids":["cv"],"evidence":"The portal displays the selected CV filename and upload-complete status."}
```

6. Inspect the Next/Save action's purpose. Advance only if it continues editing.
   Pressing Enter can submit a form, so do not use it merely to finish typing.
   Retry a failed non-submission action at most twice with fresh inspection;
   otherwise hand over the exact unresolved widget to the user.

## Handoffs and resume

```json
{"type":"block","reason":"captcha","detail":"Complete the challenge in the connected Edge tab, then say resume."}
```

Reasons include login, signup, captcha, mfa, verification, missing-input,
unsupported, and session-expired. Reuse existing browser sessions; ask before
new account creation. The user completes credentials/CAPTCHA/MFA/email steps in
the browser. The assistant continues after the user confirms and the page shows
the expected state. Persistent blocks remain blocked; no bypass or solver.

```json
{"type":"resume"}
```

Resume clears the handoff but marks previous sections/uploads `needs-recheck`.
Inspect actual retained portal data and verify again. Do not assume the browser
or server kept a draft. Update `selected_documents` using a `select` event if a
combined document or new version changes the user's chosen file set; reverify
the portal's attachment list and remove obsolete attachments explicitly.

```json
{"type":"select","document_ids":["cv","other"]}
```

## Final review

There may be a review page, or the last editing page may contain the final send
button. In either case stop before sending. Record the final observation only
after checking the exact target and all visible errors:

```json
{"type":"observe","url":"https://example.invalid/jobs/42/review","company":"Example Employer","reference":"42","final_action":"submit_application","validation_errors":[],"evidence":"Target role confirmed; all sections complete; next action sends this application."}
```

`final_action` is `continue`, `submit_application`, or `unknown`. Unknown actions
cannot pass the review check. A different company/reference is rejected. Record
public vacancy URLs rather than authentication callbacks.

```sh
python scripts/cvtool.py application review --workspace "../career/applications/example-42"
python scripts/cvtool.py application status --workspace "../career/applications/example-42"
```

Review exits nonzero and lists issues until all inventoried sections are
verified, missing/unconfirmed fields are empty, selected file hashes match,
upload rules/completion checks pass, and the final application action has been
observed. File changes invalidate readiness. `status` is read-only and reports
current issues as well as the saved phase.

The final result is **ready for review**. Show the user important answers,
filenames, remaining declarations, and the manual Submit/Apply action. Never
claim submission or a receipt. Skill instructions and the ledger are not a
security boundary around arbitrary browser tools: the host must honor the
review-only workflow, and the user supervises the actual portal.
