# Signal Lab: open catalog and MCP examples

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24401248.svg)](https://doi.org/10.5281/zenodo.24401248)

[Signal Lab](https://signal-lab.qdt.ai) is a growing catalog of free data sources, updated daily, built for AI agents first and people too. Each entry records what the source offers, what sign-up it needs, its licence (with the fine print read for you) and the result of a daily, polite reachability check.

This repository holds the open part: a catalog snapshot you can download, the published scoring method, and small examples for calling the public MCP server. The live site is the source of truth.

## Connect the MCP server

Endpoint: `https://signal-lab.qdt.ai/api/mcp` (streamable HTTP, **no authentication**, 27 read-only tools).

**Claude Code**
```bash
claude mcp add --transport http signal-lab https://signal-lab.qdt.ai/api/mcp
```

**Claude Desktop / Claude.ai**: Settings → Connectors → add a custom connector with the URL above.

**Cursor**: add to `~/.cursor/mcp.json` (or `.cursor/mcp.json` in a project):
```json
{ "mcpServers": { "signal-lab": { "url": "https://signal-lab.qdt.ai/api/mcp" } } }
```

**Other MCP clients**: point any client that supports streamable HTTP at the URL. No API key or header is needed.

The same server config is in [`.mcp.json`](.mcp.json) at the repo root (Open Plugins layout), so plugin directories and clients that read it can set Signal Lab up from this repo.

Useful first calls: `list_filters` (valid filter values), `search_catalog`, `get_entry`, `compare_entries`, `export_catalog`, `whats_new`. See the [examples](examples/).

## Add Signal Lab to your AI assistant

Signal Lab is a growing catalog of free data sources, updated daily. The server needs no API key or sign-in. In every client below, use the endpoint `https://signal-lab.qdt.ai/api/mcp`.

**Gemini CLI**: install the extension from this repo, then restart the CLI.

```
gemini extensions install https://github.com/quantumdatatechnologies/signal-lab-catalog
```

**Mistral Le Chat** ([docs](https://docs.mistral.ai/vibe/work/connectors/mcp-connectors)): adding a connector needs an administrator (on Free, Pro and Student plans the account owner is the administrator). Open `Connectors`, click `+ Add Connector`, switch to the `Custom MCP Connector` tab, enter a name without spaces (for example `signal-lab`) and the endpoint as the Server URL, then click `Connect`. Mistral detects that no authentication is needed.

**Perplexity** ([docs](https://www.perplexity.ai/help-center/en/articles/13915507-adding-custom-remote-connectors)): custom remote connectors are limited to paid plans (Pro, Max and Enterprise). Open `Plugins` in the sidebar, choose `Add custom`, then `Add MCP connector`, then `Remote`. Enter a name and the endpoint as the MCP server URL. Under `Advanced`, set `Authentication` to `None` and `Transport` to `Streamable HTTP`.

**Microsoft Copilot Studio** ([docs](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent)): on your agent's `Tools` page, select `Add a tool`, then `New tool`, then `Model Context Protocol`. Fill in the server name, a short description and the endpoint as the Server URL, set authentication to `None`, and select `Create`.

**Claude and Cursor**: see the setup steps above.

## Data

`data/catalog.json` and `data/catalog.csv` are a snapshot of the catalog, regenerated every day by a GitHub Actions workflow that runs `scripts/refresh.py` against the public MCP server. Columns include `id`, `name`, `url`, `licence`, `licence_url`, `licence_note`, `auth`, `badge`, `category`, `domain`, `type`, `description`, `free_tier_limits`, `rate_limits`, `docs_url`, `signal_lab_url`, `tasks`, `last_verified` and `attribution`. The `meta` block in the JSON file records the source and generation time.

The same data is available live at [catalog.json](https://signal-lab.qdt.ai/catalog.json) and [catalog.csv](https://signal-lab.qdt.ai/catalog.csv).

**Licence caveat:** the catalog as a compilation is CC BY 4.0, but every listed source keeps its own licence and terms. Check the `licence` and `licence_note` for each entry and the provider's terms before reuse. See [LICENSE-DATA.md](LICENSE-DATA.md).

## Methodology

Entries are checked once a day and given a measured score (v2) built only from measurements and reviewed licence and auth fields. Summary and link: [methodology/README.md](methodology/README.md).

## Contribute

Know a free source we are missing, or see something wrong? Open an issue or email signal-lab@qdt.ai. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

Code: [MIT](LICENSE). Data: [CC BY 4.0](LICENSE-DATA.md) with the per-entry caveat above.

Information and education only. Not financial, investment, legal or tax advice. Free tiers, limits and licences belong to the data providers and can change; Signal Lab is not affiliated with or endorsed by any provider. Signal Lab is operated by Quantum Data Technologies Ltd.

## How to cite

Quantum Data Technologies (2026). *Signal Lab: free data sources for AI agents (catalog snapshot)*. Zenodo. https://doi.org/10.5281/zenodo.24401248

This DOI always resolves to the latest version. A `CITATION.cff` file is included for reference managers and GitHub's "Cite this repository" button.
