---
name: tailored-resume-generator
description: >-
  Tailor a resume, CV, or Lebenslauf to a particular job advertisement using
  supplied candidate evidence. Use for role-specific CV revisions, German
  applications, student or tech roles, and ATS-friendly formatting. Company
  research, cover letters, interview preparation, and form filling are optional
  separate skills, activated only when requested.
license: MIT
compatibility: OpenCode; optional Python 3.11+ document helpers
metadata:
  version: "2.0.0"
---

# CV Tailor

Produce a truthful, role-specific CV. Follow `references/common.md` for language,
evidence, optional-module routing, and local artifact rules. Resolve all paths
relative to this skill's directory, not the user's current project.

## Inputs and scope

Use the job advertisement plus a supplied CV, career profile, files, or chat.
Ask only for missing information that materially changes the result. If the
request is to build or update a general CV without a target job, use `master-cv`
if installed. If it is unavailable, follow the general-CV workflow in
`references/master-profile.md`; a job advertisement is not a prerequisite.

Do not launch research, generate a cover letter, prepare interviews, browse an
application portal, or install anything just because the user requested a CV.
After delivering the CV, optionally mention these next actions once. A prompt
such as "CV only" suppresses that offer.

## Workflow

1. **Identify the application.** Extract title, employer, destination country,
   career stage, reference number, language requirements, deadline, requested
   documents, and submission instructions. A branded company website does not
   prove which ATS operates the application. Use `unknown` without evidence.
2. **Map requirements to evidence.** Build a working matrix with requirement,
   priority (must/should/nice), candidate fact/source, status, and placement.
   Status is direct, transferable, unconfirmed, or gap. Missing from a CV means
   unconfirmed until the candidate clarifies. Do not put this matrix in the CV.
3. **Use optional research only when requested.** Consume an existing company
   brief or invoke `company-research`. Keep citations and uncertainty in the
   brief; do not manufacture interest, cultural fit, or experience from company
   marketing. Public company information cannot override candidate facts.
4. **Choose emphasis.** Students normally lead with current education or their
   strongest project; professionals lead with relevant experience; technical
   candidates group actual tools and show their application. Retain chronology
   for career changers. For public-sector roles, make formal eligibility and
   requested evidence easy to locate.
5. **Write the CV.** Use a concise optional summary, relevant achievements,
   education, skills, and useful projects. Reorder emphasis, not facts. Use
   concrete qualitative outcomes when metrics are unavailable. Preserve actual
   titles and dates; identify personal, academic, and paid work accurately.
6. **Localize and format.** Read `references/germany-standards.md` for Germany,
   `references/ats-germany.md` for portal submissions, and
   `references/ats-keywords-de.md` for terminology. English is the default;
   an English CV for a German role still uses English section headings.
7. **Deliver or export.** Use `references/templates.md`. For real PDF/DOCX files,
   follow `references/documents.md` and validate the exported text. The helpers
   produce actual files; they do not measure an ATS score or verify a recruiter's
   private configuration.

## Formatting decisions

- Use a single reading column, standard headings, and contact details in the
  document body. A German tabellarischer Lebenslauf is structured chronology;
  it does not require a sidebar, table object, or date column. Plain stacked
  role/employer/date lines work for student, technical, and English CVs too.
- One page is a useful student target, not a hard rule. One or two pages works
  for most professionals; inspect the actual export before claiming page count.
- Follow the portal's accepted format. Text-based PDF and DOCX are both useful;
  do not infer a mandatory format from a vendor name.
- Retain `Present` for genuinely ongoing roles. Do not fabricate an end date to
  appease a parser. Preserve German characters and the spelling of proper names.
- Dates, photos, signatures, personal data, certificates, and grade conventions
  depend on the employer and destination country. Do not import German rules
  into Austria or Switzerland automatically.

## Output and final check

Return the requested CV first, then a short change summary, substantive gaps,
and facts needing confirmation. Label incomplete drafts clearly. A final CV
contains no `[confirm]` or `[metric needed]` placeholders. Do not require a
number in every bullet or a certificate for every self-reported skill.

Verify that every claimed qualification is supported, dates and titles agree
with the input, and required eligibility is either evidenced or left visibly
unresolved. Keep the master profile unchanged unless the user asked to update
it. Save this application's version separately.

Optional modules accept their own inputs and are never mandatory predecessors:
`master-cv`, `company-research`, `cover-letter`, `interview-prep`, and
`application-assistant`.
