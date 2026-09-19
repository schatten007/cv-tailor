---
name: tailored-resume-generator
description: Use when tailoring a resume, CV, Lebenslauf, Anschreiben, cover letter, or application package to a job description, especially for Germany/DACH, ATS, career transitions, student roles, or tech roles. Maps requirements to truthful evidence and produces market-appropriate documents with gap analysis and interview guidance. Trigger terms: tailored resume, CV, Lebenslauf, Bewerbung, Anschreiben, cover letter, job description, ATS, Germany, DACH, Werkstudent, Praktikum, career transition.
license: MIT
---

# Tailored Resume Generator

Tailor application documents to a specific role without inventing experience.
The job advertisement is the source of truth for requirements, terminology,
language, document requests, and submission constraints.

## Operating Defaults

- Explanations and generated documents default to English. Use German when the
  user requests it or when the employer requires German-language application
  documents. A German-language advertisement alone is a reason to note the
  expectation, not to switch languages automatically. Keep the advertisement's
  German terms in the keyword map either way, and let established technical or
  professional terms appear naturally in any language.
- Use headings and section labels in the chosen document language, and keep one
  language within each document.
- Apply Germany-specific rules when the role, employer, portal, location, or
  user mentions Germany, Deutschland, Lebenslauf, Bewerbung, Anschreiben,
  Arbeitszeugnis, Werkstudent, or public-sector German employment. Scope
  country-specific legal, salary, and document rules to the destination
  country; do not assume Austrian or Swiss practice from a German rule.
- Ask for missing information when it materially affects accuracy or
  submission; otherwise draft with the evidence available and flag what still
  needs confirming.
- Preserve the candidate's facts. Use `[metric needed]` or `[confirm]` in
  labelled drafts rather than manufacturing numbers, proficiency levels, dates,
  qualifications, language ability, visa status, or achievements. A
  submission-ready version should contain completed wording or an honest
  omission, not leftover placeholders.

## What This Skill Produces

Depending on the request and job-ad requirements, produce:

1. A tailored resume/CV/Lebenslauf.
2. A conditional Anschreiben or cover letter, only when required or useful.
3. A short application email or portal motivation answer when no cover letter
   is requested.
4. An attachment plan for Zeugnisse, Arbeitszeugnisse, certificates, and
   portfolios.
5. A requirement-to-evidence matrix, gap analysis, and prioritized revisions.
6. Interview talking points, cover-letter hooks, and follow-up questions.

## Workflow

### 1. Gather Inputs

Request or identify:

- Full job advertisement, including language, requirements, reference number,
  requested documents, salary wording, and earliest start date.
- Company, job title, location, sector, company type, and application channel.
- Existing resume or complete work history with roles, employers, locations,
  dates, responsibilities, tools, scope, and measurable outcomes.
- Education, certifications, projects, publications, languages with honest
  CEFR levels, and relevant Arbeitszeugnisse or other evidence.
- Target market, preferred output language, career stage, and document format.
- Availability, work authorization or qualification-recognition details only
  when relevant to the role or explicitly requested.

Do not request age, marital status, religion, health data, family details, or a
photo unless the user wants to discuss an optional Germany-specific choice.

### 2. Infer the Application Profile

Determine these before writing:

1. **Language:** Follow the Operating Defaults language policy (English unless
   the user requests German or the employer requires German documents). Keep a
   single language within each document; do not create mixed German-English
   headings.
2. **Sector:** Classify as enterprise, Mittelstand, public sector, startup/scaleup,
   regulated employer, creative role, or another clear profile.
3. **Career stage:** Student/Werkstudent/Praktikum, graduate, professional,
   senior/executive, or career changer.
4. **Submission route:** Direct human referral/email, company portal, job board,
   or unknown ATS. Treat a portal as ATS-mediated by default.
5. **Document request:** Required, optional, or not requested for Anschreiben,
   photo, salary expectation, start date, certificates, portfolio, and references.

For any portal submission, read `references/ats-germany.md` and apply its
parse-safe defaults. If the user names a specific ATS or portal, use that
system's notes and any stated format requirements.

### 3. Analyze and Map Requirements

Create an internal matrix with one row per requirement. Do not copy the matrix
into the resume or application document:

| Requirement | Priority | Exact term | Candidate evidence | Strength | Placement |
| --- | --- | --- | --- | --- | --- |
| Required skill or qualification | Must / should / nice | Wording from ad | Fact, role, project, or certificate | Direct / transferable / unconfirmed / gap | Profile / experience / skills / letter |

Evidence strength:

- **Direct:** supported by supplied experience, a qualification, or a
  certificate.
- **Transferable:** an adjacent skill or context supports it.
- **Unconfirmed:** plausibly true but not in the supplied material. Ask rather
  than assume the candidate lacks it. A skill missing from the CV is not
  automatically a gap.
- **Gap:** the candidate does not have it. Treat candidate statements and honest
  self-assessments as evidence; a certificate is relevant when the process asks
  for one.

Extract and prioritize:

- Must-have qualifications, formal degrees, licenses, and years of experience.
- Tools, methods, systems, domain terms, language levels, and job-title terms.
- Repeated terms and phrases likely used for ATS matching.
- Scope signals: team size, budget, revenue, geography, customer volume, and
  seniority.
- Soft skills only when the candidate can prove them through an example.
- Company and sector signals: regulated, tariff-bound, public, international,
  startup, or Mittelstand.
- Missing, ambiguous, conflicting, or unverifiable requirements.

Use exact job-ad terminology only when the candidate can substantiate it. Add an
acronym and its full form when useful, such as `SQL (Structured Query Language)`.
Never turn a partial match into a direct claim.

### 4. Choose the Document Structure

#### Germany default: tabellarischer Lebenslauf

The German "two-column" convention means a visual date-left/content-right
alignment, not a real table or a sidebar. Implement it as one linear reading
flow with tab stops or indentation. Never use a Word/HTML table, a floating
sidebar, or text boxes for core content because ATS parsers can interleave or
drop the fields.

Use:

- A4 page size for German documents.
- Reverse chronology within experience and education.
- `MM/YYYY - MM/YYYY` or a consistent German month/year equivalent.
- Explicit, honest labels for gaps: `Jobsuche`, `Weiterbildung`, `Elternzeit`,
  `Sprachkurs`, or another accurate label.
- A short Kurzprofil under contact details when it improves role positioning.
- Hard skills, tools, methods, and CEFR language levels over unsupported
  soft-skill lists.
- One page for most students and early-career candidates; one to two pages for
  professionals. Add a page only when it contains relevant evidence.
- Place, date, and signature at the end only when appropriate for the German
  process; it is customary in formal applications but not a legal requirement
  and should not be forced into international or ATS portal variants.

#### Student, Werkstudent, Praktikum, and graduate variant

- Usually one page.
- Put `Ausbildung / Studium` first when it is the strongest qualification.
- Include degree, university, expected completion, relevant modules or grade
  only when useful, then projects, Praktika, HiWi/Tutorium, and relevant jobs.
- Describe each project or placement using task, contribution, tools, and result.
- Add hours/start availability only when the role requests or benefits from it.
- Keep photo, date of birth, and signature optional; omit them for tech,
  international, anonymized, and ATS-first applications.

#### Tech and international English variant

- Use a single-column layout even when the employer uses a modern ATS.
- Put a concise summary and grouped technical skills near the top.
- Use impact-focused bullets with technologies, scope, and outcomes.
- English is the default; if the advertisement or process clearly requires
  German documents, flag that and offer a German version. Do not translate a
  German CV word-for-word.
- Usually omit photo, date of birth, marital status, and other unnecessary
  personal data.
- Include GitHub, portfolio, publications, or relevant open-source work when
  they prove the target requirements.

#### Public-sector variant

- Treat the requirement profile as a formal checklist.
- Use the exact terms from the announcement and explicitly evidence each
  mandatory criterion.
- Expect a complete document package, strict deadlines, and an Anschreiben.
- Avoid creative layouts and do not omit a required certificate or form.
- Do not add a salary expectation when compensation is fixed by TVöD/TV-L
  unless the announcement explicitly asks for one.

Read `references/germany-standards.md` for the full decision matrix and
`references/templates.md` before generating a document structure.

### 5. Draft Evidence-Led Content

#### Profile or summary

- State the target role, relevant experience level, strongest requirements, and
  value proposition in two to four lines.
- Use the job title from the advertisement when truthful.
- Avoid generic claims such as "results-driven team player" without evidence.

#### Skills

- Group skills by the job's logic: languages, tools, platforms, methods,
  domain knowledge, certifications.
- Put required skills first, but include only substantiated skills.
- Use plain text, not bars, stars, icons, logos, or visual ratings.
- For German ads, use the German term from the ad and add the established
  English term or acronym where it improves matching.

#### Experience

- Prioritize the most relevant bullets within each role.
- Use `action + context/tool + scope + result`.
- Use measurable results when figures are available; otherwise write a concrete
  qualitative bullet. A bullet without a number is still useful. Never invent
  metrics, and ask for a figure only when it materially strengthens a key
  requirement.
- Explain unfamiliar employers or foreign qualifications briefly when that
  context helps a German recruiter.
- Preserve chronology and employment dates; do not hide a material gap.

#### Education, certificates, and evidence

- Keep formal qualifications visible when they are requirements.
- Explain foreign degrees with the original title plus a plain-language
  equivalent only when supported by the candidate or an official evaluation.
- Recommend `anabin` or ZAB evidence for international applicants when relevant;
  do not claim equivalence without verification.
- Separate the core CV from Anlagen. Do not write "references available upon
  request" as a substitute for German Arbeitszeugnisse.

### 6. Apply ATS Hardening

For any portal submission, read `references/ats-germany.md`. Prefer a simple,
parse-friendly layout by default:

- Single linear reading column; avoid tables, sidebars, text boxes, floating
  elements, graphics, or multi-column layout for core content.
- Contact details in the document body, not headers or footers.
- Standard headings in the document's language.
- Plain text skills and standard bullets.
- Consistent dates and one role per title entry.
- Standard fonts at a readable size; no spaced-out headings or decorative fonts.
- Follow the portal's accepted formats. Use a text-selectable PDF or DOCX;
  never a scanned or image-only file.
- Use important job-ad terminology naturally; truthful equivalents are fine.
- No hidden keywords, white text, keyword stuffing, or copied requirements that
  the candidate cannot prove.

Assess the exported document's extracted text and reading order before sending
(a copy/paste check into a plain-text editor is a quick approximation, not a
guarantee of how a specific ATS parses it). When the portal exposes autofilled
fields, verify them.

If the portal states a preferred or required format, follow it. Where both DOCX
and PDF are accepted, a clean DOCX is a safe default; if PDF is required, export
a text-based PDF from a normal document editor. Treat an unidentified ATS as
unknown and apply these general defaults rather than guessing vendor behavior.

### 7. Decide on Germany-Specific Components

#### Photo

Never make a Bewerbungsfoto mandatory. It is legally voluntary. Offer a
professional photo as an explicit, contextual choice for classic German
Mittelstand, client-facing, banking/insurance, hospitality, healthcare, or
leadership applications. Omit it for public-sector/anonymized procedures,
tech/startups, international processes, US/UK-style applications, or when the
photo is not high quality. Do not leave a blank photo placeholder.

#### Anschreiben

Generate it when the advertisement asks for it, says `vollständige
Bewerbungsunterlagen`, the process has a mandatory field, or the candidate needs
to explain a career change, gap, relocation, leadership motivation, or an
unsolicited application.

If optional, prefer a 150-250 word version or a short portal motivation answer
over a generic full-page letter. Use a specific salutation, direct opening,
evidence tied to the key requirement, motivation, and a closing with availability
and salary only when requested. Apply DIN 5008-style formatting to a formal
German Anschreiben; it is guidance, not law.

#### Salary and availability

- Add a salary expectation only when requested or strategically appropriate.
- Use the pay unit and currency that fit the role and the candidate's
  information: gross annual salary in euros for most German roles, but follow an
  hourly or monthly basis when that is how the role is paid (for example a
  Werkstudent or Minijob). Normally give a range, place it in the closing
  paragraph of the Anschreiben, and never put it in the CV.
- Add the earliest start date when requested. Use a confirmed date when the
  candidate provides one; otherwise state the known notice period and its
  condition (for example, availability after a stated notice period) rather than
  inventing a specific date.
- Do not write `ab sofort` / "immediately available" for an employed candidate
  unless true.

#### Attachments

Recommend only relevant evidence. A typical German package is Anschreiben,
Lebenslauf, then selected Arbeitszeugnisse, highest relevant education proof,
and relevant certificates. The latest or strongest work reference usually comes
first. Follow portal upload fields instead of forcing one merged PDF when the
portal separates documents.

### 8. Report Results and Gaps

Return the finished document first, then:

1. **Tailoring decisions:** market, language, sector, career stage, and ATS
   assumptions.
2. **Strengths:** direct matches and distinctive evidence.
3. **Gaps and risks:** unmet requirements, missing metrics, uncertain
   equivalence, missing documents, language or availability constraints.
4. **Verification requests:** facts the candidate must confirm before use.
5. **Application package:** Anschreiben, email/portal answer, attachments, and
   portfolio recommendations.
6. **Interview preparation:** three to five evidence-based stories and targeted
   questions for the employer.

Do not hide material gaps. A truthful transferable-skill explanation is better
than a fabricated match.

## Quality Gate

Before finalizing, verify:

- Every must-have requirement is mapped to evidence, flagged as unconfirmed, or
  explicitly marked as a gap.
- Every keyword in the output is truthful and used in context.
- Dates, titles, employers, grades, language levels, and metrics are consistent.
- The document language follows the Operating Defaults policy (English unless
  German was requested or is required).
- A submission-ready document contains no leftover `[metric needed]` or
  `[confirm]` placeholders.
- German mode uses the correct document package and personal-data choices.
- The file is one or two pages only when the content supports that length.
- The ATS-safe text extraction is in the intended reading order.
- No private or sensitive information was added without a reason.
- The candidate reviews legal, factual, translation, and submission requirements
  before sending.

## Reference Files

- `references/germany-standards.md` - German market decision rules and sector
  variants.
- `references/ats-germany.md` - ATS systems, parser risks, and pre-flight rules.
- `references/templates.md` - ATS-safe German, English-tech, student, and
  Anschreiben structures.
- `references/ats-keywords-de.md` - German/English headings, keyword mapping,
  and terminology rules.

## Privacy Note

Application materials contain personal and professional data. Use only what is
needed for the target process, avoid exposing sensitive data unnecessarily, and
review every generated document for accuracy before submitting it.
