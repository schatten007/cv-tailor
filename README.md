# Tailored Resume Generator (OpenCode Skill)

An [OpenCode](https://opencode.ai) skill that turns a job advertisement plus a
candidate's real background into a market-appropriate, ATS-safe application
package: a tailored resume/CV/Lebenslauf, a conditional cover letter/Anschreiben,
an attachment plan, a requirement-to-evidence gap analysis, and interview prep.

It is deliberately **evidence-led and anti-fabrication**: it maps every job
requirement to real candidate evidence and refuses to invent metrics,
qualifications, language levels, or visa status.

It has first-class support for the **German / DACH** market (Lebenslauf,
Anschreiben, Bewerbungsfoto/AGG, Arbeitszeugnisse, salary and start-date
conventions, foreign-degree recognition) while remaining usable for
international and tech applications.

---

## What it does

- **Tailors to the ad.** Extracts must-have vs. nice-to-have requirements,
  exact terminology, and scope signals, then maps each to candidate evidence
  graded Direct / Transferable / Unconfirmed / Gap.
- **Never fabricates.** Uses `[metric needed]` / `[confirm]` placeholders in
  drafts; a submission-ready document must have completed wording or an honest
  omission (enforced by a final Quality Gate).
- **Hardens for ATS.** Single-column, parse-safe layout; standard headings;
  consistent dates; contact details in the body; no tables/sidebars/graphics in
  core content; DOCX/PDF guidance; per-system notes for the ATS common in
  Germany.
- **Applies German market rules.** Correct `tabellarischer Lebenslauf` structure
  (a *visual* date-left/content-right split, not a real table), conditional
  Anschreiben, contextual photo decisions, salary/availability conventions, and
  Anlagen ordering.
- **Adapts by profile.** Distinct handling for student/Werkstudent/Praktikum,
  graduate, professional, senior, career-changer, tech/English, and
  public-sector applications.
- **Reports gaps and next steps.** Strengths, risks, verification requests, and
  three to five interview stories.

## Language policy

Explanations and generated documents default to **English**. The skill switches
to **German** when the user asks or when the employer requires German-language
documents, and it always preserves the advertisement's German terms in the
keyword map. It keeps a single language per document.

---

## Installation

OpenCode auto-discovers skills from its skill directories. Pick one:

### Global (available in every project)

```bash
# macOS / Linux
git clone https://github.com/<you>/tailored-resume-generator \
  ~/.config/opencode/skills/tailored-resume-generator
```

```powershell
# Windows (PowerShell)
git clone https://github.com/<you>/tailored-resume-generator `
  "$env:USERPROFILE\.config\opencode\skills\tailored-resume-generator"
```

### Per project

Copy the `tailored-resume-generator/` folder into your repo at
`.opencode/skills/tailored-resume-generator/`.

### Via config path

Point `skills.paths` at wherever you keep it:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": ["~/dev/opencode-skills"]
  }
}
```

The folder **must** contain `SKILL.md`, and the `name` in its frontmatter must
match the folder name (`tailored-resume-generator`).

**Restart OpenCode after installing or editing the skill** — skills are loaded
at startup and are not hot-reloaded.

### Verify

Start OpenCode and confirm the skill is listed (it appears in the available
skills), then trigger it with a request such as *"Tailor my CV to this job ad."*

---

## Usage

The skill activates on requests about resumes, CVs, Lebenslauf, Anschreiben,
cover letters, ATS optimization, or German/DACH applications. Give it:

1. The **full job advertisement** (language, requirements, requested documents,
   salary wording, start date, reference number).
2. Your **background** — an existing resume or a work history with roles,
   employers, dates, tools, scope, and outcomes; education; certifications;
   languages with honest CEFR levels; relevant Arbeitszeugnisse.
3. Any **preferences** — target market, output language, career stage, format.

Example:

```
Tailor my CV to this Werkstudent Data Analytics role in Munich.
[paste job ad]
Here is my background:
[paste resume or history]
```

The more concrete evidence you provide (numbers, scope, tools), the stronger the
result. The skill will ask for anything that materially affects accuracy and
flag what still needs confirming.

---

## Files

| File | Purpose |
| --- | --- |
| `SKILL.md` | Entry point: operating defaults, workflow, quality gate. |
| `references/germany-standards.md` | German market decision matrix, CV/Anschreiben/photo/Anlagen rules, career-stage variants, international applicants. |
| `references/ats-germany.md` | ATS parse-safe checklist and per-system notes (SuccessFactors, Workday, Personio, softgarden/rexx/d.vinci, Greenhouse/Lever/Ashby, Taleo/iCIMS), with vendor sources. |
| `references/templates.md` | ATS-safe document skeletons: German Lebenslauf, student, English-tech CV, Anschreiben, application email, attachment plan. |
| `references/ats-keywords-de.md` | German/English heading pairs, keyword extraction/mapping rules, keyword families, quality gate. |

Reference files are loaded on demand by `SKILL.md`, so the skill stays lean until
a given concern (German rules, ATS hardening, templates, keywords) is relevant.

---

## Scope and limitations

- **Not legal, tax, or immigration advice.** German legal, salary, and
  document rules are provided as guidance; the candidate confirms current
  requirements before submitting.
- **Germany-focused.** Austria is broadly similar; Switzerland differs. Do not
  assume AT/CH practice from a German rule.
- **ATS behavior is not guaranteed.** Parser notes are documented or commonly
  reported behavior and vary by configuration. The copy/paste extraction check
  approximates parsing; it does not replicate a specific vendor's parser.
- **The candidate owns the truth.** The skill will not invent experience; you
  must supply and verify the facts.

## Sources

Per-system ATS notes prefer primary vendor documentation (Personio, Workday,
Greenhouse, SAP SuccessFactors KBA), supplemented by lower-confidence résumé
guidance. See the Sources section of `references/ats-germany.md` for the list.

## License

Add a license before publishing (MIT is a common choice for skills). Include a
`LICENSE` file in the repository root.
