---
name: cover-letter
description: >-
  Write or revise an Anschreiben, cover letter, application email, or portal
  motivation answer when explicitly requested. Works from any supplied CV or
  career facts plus role information; optionally uses company research. Do not
  activate merely because a CV was created.
license: MIT
compatibility: OpenCode; optional Python 3.11+ document helpers
metadata:
  version: "2.0.0"
---

# Cover Letter / Anschreiben

Read `../../references/common.md`, `../../references/germany-standards.md`
when relevant, and `../../references/templates.md`. Existing CVs and chat facts
are valid inputs; no other module has to run first.

## Workflow

1. Identify the actual deliverable: letter, short email, motivation answer, or
   answers to separate portal questions. Follow explicit word/character limits.
   A request for a CV alone does not activate this skill.
2. Extract the key requirements and the candidate's strongest matching evidence.
   Ask for missing facts only when they change the letter substantially. The
   letter should add motivation and context, not narrate the entire CV.
3. Use a supplied company brief if available. Offer company research once if
   it would add value; run `company-research` only when selected. If declined or
   unavailable, use the ad and known facts without pretending research occurred.
4. Build 2-3 specific writing points: company/role fact -> candidate evidence ->
   credible contribution. Keep uncertain company claims out of confident prose;
   do not invent the candidate's enthusiasm, preferences, or values.
5. Write a direct opening, a concrete proof paragraph, a specific employer/role
   connection, and a concise close. English is the default unless German is
   requested or required. For formal German letters use correct German spelling
   and a DIN-5008-inspired structure, not a claim of mandatory formatting.
6. Mention salary only when requested or chosen by the user; preserve hourly,
   monthly, or annual units and gross/net meaning. Use a confirmed start date
   or the actual notice-period condition, never a guessed calendar date.
7. Return the letter first and a brief rationale/confirmation list separately.
   Use actual known recipient details or a neutral salutation. Remove every
   draft placeholder from a final version. For files read
   `../../references/documents.md` and export a real PDF/DOCX.

A voluntary letter often fits 150-250 words; an explicit employer limit wins.
Evidence and the user's voice matter more than a rigid formula. Research
citations normally stay in a companion rationale, not in the application letter.
