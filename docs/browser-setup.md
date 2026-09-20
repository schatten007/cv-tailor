# Connect your existing Edge browser

Application filling is optional. The writing modules need no browser setup.

1. Install [Microsoft's Playwright extension](https://chromewebstore.google.com/detail/playwright-extension/mmlmfjhmonkocbjadbfplnigmagldckm)
   in the Edge profile where you use your job-portal accounts. Chrome is also
   supported. If Edge asks, allow extensions from the Chrome Web Store.
2. Install a supported Node.js release if needed (Playwright MCP requires Node
   18+; Node 22/24 LTS is suitable). Ask permission before changing another user's
   setup or installing any dependency.
3. Merge this entry into the `mcp` object of your OpenCode config. Do not replace
   your existing configuration. On Windows use `npx.cmd` if `npx` resolves to a
   PowerShell script blocked by execution policy.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "playwright": {
      "type": "local",
      "command": ["npx", "-y", "@playwright/mcp@0.0.82", "--extension"],
      "enabled": true
    }
  }
}
```

4. Quit and restart OpenCode. Open the intended job application in Edge. On the
   first browser-tool connection, use the extension's connection/tab-selection
   page to choose that tab and approve access. If the wrong profile opens,
   follow the extension's profile-selection documentation; do not copy cookies
   or a live browser profile into the repo.
5. Ask: **"Fill this application using these final documents. Stop before
   submitting."** Keep the connected browser available for login, CAPTCHA,
   Cloudflare challenges, MFA, and email-verification handoffs.

The example pins a known release for repeatability. The agent checks actual
tool schemas; other browser MCP servers work only if they expose equivalent
snapshot, fill, select, upload, and wait capabilities. Never assume the same
tool-name prefix. For a remote browser, local upload files need an explicitly
approved transfer; a local server is simpler for personal applications.

The application workspace must be accessible under the MCP workspace roots.
Use a normal local career workspace rather than enabling unrestricted access.
The extension attaches Edge/Chrome sessions; it cannot attach a Safari/Firefox
default browser. New accounts are created only with your choice, and passwords
stay in the browser.

Sources:
- https://github.com/microsoft/playwright-mcp
- https://github.com/microsoft/playwright/tree/main/packages/extension
- https://opencode.ai/docs/mcp-servers/
