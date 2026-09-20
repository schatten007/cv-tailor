# Optional setup and browser connection

Plain writing skills work with supplied material and the host's normal tools.
Python helpers, research suites, and browser MCP servers are optional capabilities.
Installing a SKILL.md does not install an MCP or grant it permissions.

## Permission-based dependency setup

1. Discover actual exposed tools/skills; optionally run `scripts/cvtool.py doctor`
   from the toolkit root for local Python/library/skill-file checks. This reports
   file discovery, not proof that OpenCode exposes a tool.
2. If something is missing, show source URL, exact version/ref when available,
   installation destination, and proposed config additions. Ask with `question`.
3. If permission is declined, continue with existing tools or supplied material.
4. If approved, install only the requested dependencies. For a research suite,
   obtain a trusted repository/ref from the user, inspect its license and install
   instructions, and copy only the selected skills. Resolve paths portably;
   check Python/PyYAML and any named subagents rather than assuming they exist.
5. Merge the necessary MCP config with the existing JSON/JSONC, preserving
   unrelated settings and comments. Never replace the entire config with an
   example. Validate against https://opencode.ai/config.json, restart OpenCode,
   and verify the new tool names and schemas before use.

The toolkit installer handles this repository's selected skills. It previews by
default and writes only with `--apply`; it refuses existing targets to protect
local modifications. It does not install third-party code or alter MCP config.

## Preferred browser: existing Edge session

Install Microsoft's Playwright browser extension in the Edge profile used for
applications. The extension also supports Chrome; Firefox/Safari cannot be
attached using this extension. If the default browser is unsupported, ask the
user to select Edge/Chrome rather than silently starting a logged-out browser.

Use a local Playwright MCP server with `--extension`. The extension connects a
selected existing tab/profile; its connection prompt must be accepted in the
browser. Do not disable connection approval. Account cookies stay in the browser.
Do not copy a live Edge profile directory or export cookies into the repository.

The config example in `docs/browser-setup.md` is for OpenCode, not the
`mcpServers` shape used by some other clients. Use a tested pinned MCP version
for a repeatable setup, or inspect the current release and tools at install time.
Discover browser snapshot/fill/select/upload/wait tools by capability; server
prefixes and parameter names vary. One connected browser is operated serially.

## Authentication and challenges

Reuse an existing logged-in employer account. Ask before signup if none exists;
fill non-secret registration facts from the candidate's confirmed profile, then
hand over password entry, email verification, MFA, and CAPTCHA to the user.
After the user completes a Cloudflare or CAPTCHA challenge, capture a fresh
snapshot and confirm the target job/account. If it remains blocked, save progress
for manual completion instead of using bypasses, solver services, or retry loops.

## File access

The browser server must be able to read the selected upload files. Prefer a
local MCP with the career workspace as an allowed workspace root. Stage only
selected documents there and pass absolute paths. With a remote MCP, local paths
do not magically exist on its host; obtain permission for an explicit transfer
or switch to a local connection. Do not enable unrestricted file access by default.

## References

- OpenCode skills: https://opencode.ai/docs/skills/
- OpenCode MCP: https://opencode.ai/docs/mcp-servers/
- Playwright MCP: https://github.com/microsoft/playwright-mcp
- Browser extension: https://github.com/microsoft/playwright/tree/main/packages/extension
