# ATS Hardening for the German Market (2025-2026)

Defensive formatting rules to help a tailored resume parse reliably in the
applicant tracking systems (Bewerbermanagementsysteme) used in Germany. Load
this when the application goes through a company portal or a job board
(StepStone, Indeed, LinkedIn, XING, Arbeitsagentur).

Assume a portal application may be machine-parsed, and prefer a simple layout by
default. When the specific system is unknown, apply the general parse-safe
checklist below rather than assuming a named vendor's behavior.

## The rule that matters most: single reading column

Many parsers flatten a document to text before extracting fields, so a true
two-column / sidebar layout (skills on the left, experience on the right) can
interleave and mis-assign fields. A single linear column avoids that risk.

- The German **tabellarischer Lebenslauf** is a *visual* date-left / content-right
  layout. Implement it with **tab stops or indentation in a single linear column**,
  not with a real table object or a two-column/sidebar template.
- "Looks like a table, built with tabs" = safe. "Word/HTML table or text boxes" = riskier.
- Quick check: open the exported file, `Ctrl+A` -> copy -> paste into a plain-text
  editor. If order is scrambled, words are glued together, or sections vanish, fix
  it before sending. This approximates extraction; it is not identical to how a
  given ATS parses the file.

## Universal parse-safe checklist

- [ ] Single-column, linear top-to-bottom reading order
- [ ] No tables, text boxes, sidebars, columns, or floating elements
- [ ] Contact details in the document **body**, never in the header/footer
      (Workday and others strip header/footer on ingestion)
- [ ] Standard German section headings: `Berufserfahrung`, `Ausbildung`,
      `Kenntnisse`, `Sprachen`, `Zertifikate`, `Projekte` (or English equivalents
      if the whole document is English) - no creative headings like "Mein Weg"
- [ ] Dates one consistent format: `MM/JJJJ - MM/JJJJ` (avoid "bis heute";
      Workday prefers `Month YYYY ... Present`)
- [ ] One role per title entry (list promotions as separate entries)
- [ ] Skills as plain, comma/line-separated text - no rating bars, stars, icons, logos
- [ ] Fonts Arial / Calibri / Helvetica / Times, >= 10 pt, normal letter-spacing
      (avoid "gesperrte" spaced-out headings - spacing can break word detection)
- [ ] Acronym **and** full term at least once: `SQL (Structured Query Language)`
- [ ] Important job-ad terminology used naturally; truthful equivalents are fine
      (many matchers map related terms, so do not force awkward exact copies)
- [ ] Text-based PDF or DOCX exported from a normal document editor, not a scan
      or image, and not a design tool that produces image-heavy output. Follow
      the portal's stated/accepted format; where both are accepted, DOCX is a
      safe default.

## Per-system notes and defensive move

These are documented or commonly reported behaviors, not guarantees. Behavior
varies by configuration, so treat them as reasons to keep the layout simple, and
verify autofilled fields when the portal shows them. Where the system is
unknown, use the universal checklist above.

| System | Segment in DE | Documented / reported behavior | Defensive move |
| --- | --- | --- | --- |
| **SAP SuccessFactors** | Large enterprise, industry | Vendor docs: parsing is imperfect; scanned/image PDFs do not parse; some flows skip header/footer; text-based files parse best. Often no candidate verification screen, so parse errors can go unseen | Single column, plain text, standard headings; text-based DOCX/PDF; do not rely on a review screen |
| **Workday** | Large enterprise | Vendor docs: parsing results vary by format and word order; best with no images/image-based styles; parsing can be hidden for external applicants. Often shows a review screen | DOCX or clean text-PDF; contact in the body; check any review screen before submit |
| **Personio** | Mittelstand (HRIS+ATS, Textkernel parser) | Vendor docs list parse-failure triggers: non-PDF/DOCX, scans/images, some ready-made templates, header/footer data, tables/multi-column, font <=8pt or uncommon fonts, graphic skills/logos | Parse-safe profile; a professional photo may still be expected in some Mittelstand contexts |
| **softgarden / rexx / d.vinci / concludis / coveto / BITE / onlyfy** | German Mittelstand & public sector | German-built; commonly report the same triggers (tables, columns, graphics, header/footer). Less public per-vendor detail | Same universal checklist; d.vinci appears often in the public sector (expect a complete, formal Bewerbung) |
| **Greenhouse / Lever / Ashby** | Berlin tech / scaleups | Generally forgiving; recruiters often see the original file alongside the parse. Greenhouse notes multi-column/table/graphic layouts as parse-failure causes; its matching maps related skill terms | Single-column is still safest; clean modern styling is usually tolerated |
| **Oracle Taleo / iCIMS** | Legacy enterprise | Commonly reported to handle columns/tables poorly and to re-key data into a form | Strict single-column; expect to re-enter data manually |

## Segment strategy (bias format by employer type)

Use these as starting biases, not certainties. If the specific system is known,
prefer its notes above; if not, apply the universal checklist.

- **Large enterprise / regulated:** strict single-column plain-text rules; DOCX
  is a safe default where accepted. Common for large corporations, industry,
  banking, insurance, and the public sector.
- **Berlin tech / scaleup:** single-column but modern styling usually
  acceptable; often English; usually no photo/DOB.
- **Mittelstand:** parse-safe layout; a professional photo is still commonly
  expected in some contexts; documents often in German.

## Interaction with other Germany rules

- **Photo:** great for a human reader, invisible/harmful to a parser. If the
  role/sector warrants a photo (Mittelstand, client-facing), keep it top-right as
  an inline image and never place text inside or behind it; for enterprise/tech/
  international or anonymised processes, omit it.
- **Language:** Keep one language per document (mixed documents tend to parse
  worse). Documents default to English; switch to German when required or
  requested, and use the ad's terminology in the keyword map.
- **Students / Werkstudenten / tech (English):** the single-column parse-safe
  rules are unchanged; only the section order changes (education-first for
  students; grouped skills/tools block forward for tech). See
  `references/germany-standards.md` and `references/templates.md` for the
  section-order variants.

## Sources

Primary/vendor documentation (retrieved 2026-09-19), preferred for the
per-system notes:

- Personio - CV parsing (formats, parse-failure triggers, Textkernel):
  <https://support.personio.de/hc/en-us/articles/360010193018-CV-parsing-for-candidate-profiles>
- Workday - Concept: Resume Parsing (format/word-order variance, images):
  <https://doc.workday.com/admin-guide/en-us/human-capital-management/recruiting/candidates/set-up-prospects-and-candidates/hdc1552497830785.html>
- Greenhouse - Unsuccessful resume parse (multi-column/table/graphic causes):
  <https://support.greenhouse.io/hc/en-us/articles/200989175-Unsuccessful-resume-parse>
- Greenhouse - Talent Matching FAQ (related-term matching, no auto-reject):
  <https://support.greenhouse.io/hc/en-us/articles/41131886674075-Talent-Matching-FAQ>
- SAP KBA 2081576 - SuccessFactors resume parsing (public preview only; full
  text requires login): <https://userapps.support.sap.com/sap/support/knowledge/en/2081576>

Secondary guidance (résumé-advice sites; treat as lower-confidence context):
resumeoptimizerpro.com, atsresumeai.com, zendikt.com, ki-bewerber-management.de,
airesume.guru, atscvchecker.pro, karrieretutor.de, myjobhub.de.

Note: adoption percentages and market-share claims from earlier drafts were
removed as unverified against primary sources.
