# ML Methods Library

A small, curated library of machine-learning and statistical methods, written for AI agents first and people too.
Each entry says what the method does, when to use it and when not to, what data it needs, and how it applies to
finance and research problems. Each one comes with a short, hand-checked set of materials instead of a list of links.

It is quality over quantity: we add methods in small reviewed batches.

## What is in an entry

Every file in `entries/` follows [`schema.json`](schema.json) (JSON Schema draft-07). Main fields:

- `id`: a stable slug, for example `garch`. IDs do not change; material IDs look like `garch:paper-1`.
- `summary`, `inputs`, `outputs`, `data_requirements`, `assumptions`, `math_summary`
- `when_to_use`, `when_not_to_use`, `pitfalls`, `compute`
- `applicability`: finance or research problems the method fits, with the Signal Lab datasets to try it on
- `materials`: 3 to 6 items: one or two key papers (with DOI or arXiv ID), one or two canonical implementations,
  one free tutorial or docs page, and one worked example on a Signal Lab dataset. Each has a one-line `why` note
  saying why we picked it.
- `facts`: the dated, machine-checked inputs behind the computed scores (citation counts, repository activity)
- `scores` and `verification`: see below

[`index.json`](index.json) lists every method with its family, task types, summary, domains, datasets and scores, so
an agent can shortlist methods without opening every file.

## How agents can use it

1. Read `index.json` and filter by `task_types`, `domains`, `sl_datasets` or scores.
2. Open the matching `entries/<id>.json` and check `when_not_to_use` and `data_requirements` against your data.
3. Start from the materials: the key paper for the theory, the implementation for code, the tutorial to learn it,
   and the worked example for a concrete first experiment on a Signal Lab dataset.
4. Check the dates in `verification` and `facts`; anything older than you are comfortable with should be re-checked.
5. Credit "Signal Lab by QDT" if you reuse the entries (CC BY 4.0).

Example in Python:

```python
import json, urllib.request
base = "https://raw.githubusercontent.com/quantumdatatechnologies/signal-lab-catalog/main/ml-methods/"
index = json.load(urllib.request.urlopen(base + "index.json"))
for m in index["methods"]:
    if "finance" in m["domains"] and m["scores"]["fit"] >= 4:
        print(m["id"], m["scores"])
```

## Scores

Six scores from 1 (low) to 5 (high). Each score records how it was set.

| Score | Set by | What it measures |
|---|---|---|
| `evidence` | code | 1 plus one point each for: a key paper with a DOI, a canonical implementation, a cited benchmark, an open abstract |
| `maturity` | code | the highest OpenAlex citation count among the key papers (200, 1,000, 5,000 and 20,000 are the steps) |
| `freshness` | code | days since the last commit to the implementation repositories (90 days, 1 year and 2 years are the steps; capped at 4 if any listed repository is over a year stale or archived) |
| `theory` | reviewer | how well founded the method is: peer-reviewed theory, clear assumptions, known guarantees |
| `ease` | reviewer | how easy it is to apply correctly: tooling, tuning burden, compute, common traps |
| `fit` | reviewer | how well it suits finance and research data such as returns, macro series and panels |

Computed scores have `"method": "code"` and an `inputs` string showing what they were computed from; the inputs are
in `facts` with the date they were checked, so anyone can recompute them. Reviewer scores have
`"method": "reviewer"`, a `status`, the `reviewer`, the date `reviewed` and a short `rationale`. A score of `null`
means there was nothing to compute it from (for example, no tracked repository).

## Verification

- Each material has a `verification` block with a status (`verified`, `no_open_link`, `broken`, `unverified`), the
  date it was `checked` and the `method` used (for example, HTTP 200 and page title checked, then read by a reviewer).
- Each entry's `verification.claim_check` records an automated comparison of the entry's claims with the key paper's
  abstract: the verdict, its scope and the date. It is a check, not proof.
- `updated` is the date the entry last changed.

## Check the files

```bash
python3 scripts/check_ml_methods.py
```

This checks required fields, the materials mix, that computed scores match their facts, that reviewed scores have a
reviewer, date and rationale, and that `index.json` matches the entries.

## Licence

CC BY 4.0 for the entries, index and schema; linked works keep their own licences. See [LICENSE.md](LICENSE.md).

Information and education only. Not financial, investment or other professional advice.
