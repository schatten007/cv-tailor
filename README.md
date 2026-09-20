# CV Tailor

An [OpenCode](https://opencode.ai) skill toolkit for job applications. It tailors
your resume/CV/Lebenslauf to a job ad **without inventing anything**, maps every
requirement to your real experience, and formats output so applicant tracking
systems (ATS) can read it. It knows the **German / DACH** rules and works for
international and tech roles too.

Optional companion skills build a master CV, research a company, write a cover
letter, prepare you for interviews, and help fill an application form in your own
browser — each usable on its own, none triggered automatically.

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
result, and it will ask about anything important that's missing.

The companion skills come bundled and activate only when you ask, e.g.
*"Build a master CV from these files"*, *"Research this company"*,
*"Write a cover letter"*, *"Prep me for the interview"*, or
*"Fill this application and stop before submitting"*.

---

## The skills

| Skill | Use it to |
| --- | --- |
| `tailored-resume-generator` | Tailor a CV to one job ad (the default). |
| `master-cv` | Build or update a general CV/profile from files and chat, no job ad needed. |
| `company-research` | Research an employer, role, and likely ATS with cited sources. |
| `cover-letter` | Write an Anschreiben, cover letter, email, or portal answer. |
| `interview-prep` | Get likely questions, evidence-backed stories, and questions to ask. |
| `application-assistant` | Fill an online application in your browser and stop before submitting. |

Each is a standalone skill. You can install only the ones you want (see below).

## What makes it careful

- **No fabrication.** It never invents metrics, titles, dates, language levels,
  or visa status. Unknowns are marked `[confirm]`; final documents ship without
  placeholders.
- **Evidence-first.** Every requirement is mapped to something you actually said
  or supplied, and gaps are shown honestly.
- **ATS-aware.** Single-column, standard headings, clean dates, real
  text-extractable files — with per-system notes for the ATS common in Germany.
- **Review-only applications.** The application assistant reuses your existing
  signed-in browser, hands control back to you for logins/CAPTCHA/MFA, and stops
  before the final Submit. It never sends an application for you.

Documents default to **English**; switch to **German** when you ask or the
employer requires it.

---

## Optional local helpers

Plain writing needs nothing extra. Real `.pdf`/`.docx` export, document staging,
and the review-only application ledger use small Python helpers in `scripts/`.

```bash
python -m venv .venv && . .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r scripts/requirements.txt
python scripts/cvtool.py doctor                    # checks deps; changes nothing
```

The helpers only ever touch local files and make no network calls. Browser
control stays with an MCP server (see below); the helpers never drive it.

## Optional: fill applications in your browser

The `application-assistant` needs a browser MCP. It is designed for Microsoft's
Playwright extension so it can reuse your **existing Edge/Chrome session** and
the accounts you are already logged into. Full setup is in
[`docs/browser-setup.md`](docs/browser-setup.md). It always stops at the review
step for you to submit manually.

## Install only some skills

Every skill is self-contained (its references, schemas, and scripts are bundled
on install). Preview first, then apply:

```bash
python tools/install.py --skills cover-letter interview-prep      # preview
python tools/install.py --skills cover-letter interview-prep --apply
```

The installer never overwrites an existing folder, so your Git clone and any
local edits are safe. Restart OpenCode afterwards.

## Files

```
SKILL.md                     Default: tailor a CV to a job ad
skills/<name>/SKILL.md       master-cv, company-research, cover-letter,
                             interview-prep, application-assistant
references/                  Germany rules, ATS notes, templates, workflows
schemas/                     JSON contracts for profiles, briefs, documents, state
scripts/                     Optional Python helpers + Playwright form helpers
docs/browser-setup.md        Connect your existing browser (optional)
examples/                    Synthetic sample records
```

## Contributing / development

```bash
pip install -r requirements-dev.txt
python -m pytest          # tests + coverage
python -m tools.check     # validate skill frontmatter, references, schemas
ruff check . && black --check . && mypy

# Optional browser E2E against the synthetic local portal fixture:
npm install
npx playwright install chromium   # or point --config at an installed msedge/chrome
npm run test:browser
```

The browser suite drives a local fixture portal through the review-only
workflow and asserts the application is never submitted
(`window.fixtureSubmissionCount()` stays `0`). If your environment blocks the
Chromium download, run it against an installed browser via a small local config
override (`use: { channel: "msedge" }`).

## Good to know

- **Not legal or immigration advice.** German rules are guidance — confirm
  current requirements before you submit.
- **Germany-focused.** Austria is similar; Switzerland differs. Don't assume.
- **ATS notes aren't guarantees.** Parser behavior varies by setup.
- **You own the facts.** It tailors your real experience; it doesn't fabricate.
- **You submit.** The assistant prepares an application; the final send is yours.

## License

[MIT](LICENSE) © 2026 schatten007
