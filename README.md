# CV Tailor

An [OpenCode](https://opencode.ai) skill that rewrites your resume, CV, or cover
letter to match a specific job ad — without inventing anything. It maps every
requirement to your real experience, flags the gaps, and formats the result so
it survives applicant tracking systems (ATS). It knows the **German / DACH**
application rules (Lebenslauf, Anschreiben, photo, Arbeitszeugnisse) and works
just as well for international and tech roles.

---

## Quick start

**1. Install** (clone into your OpenCode skills folder — keep the folder name):

```bash
# macOS / Linux
git clone https://github.com/schatten007/cv-tailor \
  ~/.config/opencode/skills/tailored-resume-generator
```

```powershell
# Windows (PowerShell)
git clone https://github.com/schatten007/cv-tailor `
  "$env:USERPROFILE\.config\opencode\skills\tailored-resume-generator"
```

**2. Restart OpenCode** (skills load at startup).

**3. Ask for it** — paste a job ad and your background:

```
Tailor my CV to this job ad.

[paste the job ad]

My background:
[paste your resume or work history]
```

That's it. The more detail you give (numbers, tools, dates), the better the
result. It will ask about anything important that's missing.

---

## What you get

- A tailored **resume / CV / Lebenslauf**
- A **cover letter / Anschreiben** — only when the role actually needs one
- A **gap analysis**: what matches, what's missing, what to confirm
- An **ATS-safe layout** that parsers can read
- **Interview prep**: talking points and questions to ask

## Why it's different

- **It won't lie for you.** No invented metrics, titles, or language levels. It
  marks unknowns with `[confirm]` instead of guessing.
- **It knows Germany.** Correct Lebenslauf structure, when a photo helps or
  hurts, salary and start-date phrasing, and which documents to attach.
- **It survives the robots.** Single-column, standard headings, clean dates —
  tuned for the ATS common in Germany (Personio, SAP SuccessFactors, Workday,
  and more).
- **It adapts.** Student/Werkstudent, graduate, professional, career-changer,
  tech, and public-sector applications each get the right treatment.

Documents default to **English**; it switches to **German** when you ask or the
employer requires it.

---

## How it's built

`SKILL.md` holds the workflow. It pulls in detail on demand from `references/`:

| File | What it covers |
| --- | --- |
| `references/germany-standards.md` | German market rules, CV/Anschreiben/photo, career-stage variants |
| `references/ats-germany.md` | ATS parse-safe checklist and per-system notes |
| `references/templates.md` | Ready-to-fill document skeletons |
| `references/ats-keywords-de.md` | German/English headings and keyword mapping |

## Alternative install (config path)

If you keep skills elsewhere, point OpenCode at the folder instead of cloning
into the default location:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": { "paths": ["~/dev/opencode-skills"] }
}
```

The folder must contain `SKILL.md`, and its frontmatter `name`
(`tailored-resume-generator`) must match the folder name.

## Good to know

- **Not legal or immigration advice.** German rules are guidance — confirm
  current requirements before you submit.
- **Germany-focused.** Austria is similar; Switzerland differs. Don't assume.
- **ATS notes aren't guarantees.** Parser behavior varies by setup.
- **You own the facts.** It tailors your real experience; it doesn't fabricate.

## License

[MIT](LICENSE) © 2026 schatten007
