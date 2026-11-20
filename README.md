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

Useful first calls: `list_filters` (valid filter values), `search_catalog`, `get_entry`, `compare_entries`, `export_catalog`, `whats_new`. See the [examples](examples/).

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
