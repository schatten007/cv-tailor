# Master profile and update workflow

No job advertisement is required. The master profile preserves useful career
evidence; a tailored CV is a selection from it, not a replacement for it.

1. Inventory supplied chat/files and assign source IDs, for example `chat-01` or
   `cv-2026`. A source label can be a filename or conversation description.
2. Record atomic facts with stable IDs and dotted field names, for example
   `identity.full_name`, `employment.job-1.title`, `education.degree-1.end_date`,
   `availability.notice_period`, or `skills.python`. Values may be strings,
   numbers, booleans, lists, or objects. Preserve actual units and date precision.
3. Set status to `confirmed`, `unconfirmed`, or `conflict`. Cite source IDs.
   Missing facts are not proof of missing skills. For a conflict retain the
   competing values with their sources; ask before choosing one.
4. Deduplicate identical evidence. The helper `profile-merge` unions identical
   sources/facts and flags conflicting values instead of selecting the newest.
   Use a distinct output filename to preserve the original profile.
5. Write a readable master CV plus a short change/confirmation list. Include
   relevant unpaid, academic, volunteer, and paid work under accurate labels.
   Persist updates when requested; keep role-specific omissions local to that CV.

Schema: `schemas/profile.schema.json` at the toolkit root (bundled into installed
skills). Source files should stay in the user's workspace, not in the public repo.
The `inspect` helper extracts text, not a guaranteed reconstruction of a layout;
review reading order and ambiguous dates before treating extraction as fact.
