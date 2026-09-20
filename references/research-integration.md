# Research skill integration

## Capability discovery

Check the agent's exposed skills/tools first. Files on disk may be denied by
permissions or unavailable until restart. Look for `research`, `research-deep`,
`research-report`, and optionally `research-add-items` / `research-add-fields`.
Check for a search tool, a fetch tool, and a browser MCP independently. A browser
MCP is not a search engine, and a research SKILL.md is not an installed MCP server.

Reuse a compatible installed suite's outline -> results -> report workflow. Pass
the company, specific role, date range, and output location explicitly. Inspect
its runtime requirements: older versions assume a `web-search` subagent, fixed
home-directory paths, Python, or PyYAML. Use only actual available agents; if
delegation fails, research directly with existing tools and record that fallback.
Do not run a hard-coded `~` Python path on Windows; resolve a quoted absolute path.

When a suite cannot support the brief contract, use it for collection and map the
results into `company-brief.schema.json`. Preserve uncertain claims in the brief
even if the suite's report skips them. Validate source references and distinguish
facts, inferences, and unknowns; field coverage is not factual verification.

## Missing dependencies

Follow `setup.md`. Ask permission before installation, naming the source/version,
dependencies, and target scope. There is no assumed universal research-skill
registry: obtain a trusted source URL/ref or user-supplied folder. Never fetch a
random same-named skill. Offer existing tools or pasted research if declined.
Do not overwrite another user's customized research suite. Restart OpenCode
after adding skills or MCP config, then verify discovery and actual tool access.

## Company brief

Record company identity, job URL, retrieval date, sources, findings, and ATS.
Every fact/inference needs source IDs. Unknowns can have no sources and must
not become assertive claims in application prose. Employee reviews are anecdotal;
company values pages express stated values, not proof of day-to-day culture.

ATS evidence: follow the public application link, observe redirects/embedded
hosts and explicit provider/privacy attribution. Record an opaque portal as
unknown; vendor detection cannot reveal parser configuration or private ranking.

For each useful cover-letter angle, connect a sourced role/company need to an
actual candidate fact. Keep hypotheses framed as questions or cautious context.
Use primary pages for current business facts, independent sources to cross-check
consequential claims, and current-year searches for recent developments.
