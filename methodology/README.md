# Methodology (summary)

Source of truth: <https://signal-lab.qdt.ai/methodology>. This is a summary; if it differs from the site, the site is right.

## The daily check
Every dataset entry is checked once a day, on Signal Lab's own compute. For each entry the check requests one URL that the entry itself lists: the data endpoint when no key is needed, otherwise the provider's page. An endpoint that needs a key is never called.

- One small request: a ranged GET for the first 64 KB only. Bulk files are never downloaded.
- `robots.txt` first. If it does not allow the request, nothing is requested and the entry shows "not requested" (counts neither as up nor down).
- HTTP 403, 429 or a bot-challenge page is recorded as "blocks automated checks" and counts neither as up nor down.
- Identified User-Agent `SignalLabCheck/1.0 (+https://signal-lab.qdt.ai/methodology; signal-lab@qdt.ai)`. No cookies, keys or sign-in. Requests to the same host are spaced out.
- Recorded: HTTP status, time to first response, Last-Modified, newest date found in the part read, format and field names seen. Sample rows are shown only when the licence allows redistribution.
- Change detection compares a short fingerprint of the part read with the previous check.

## Running the how-to
When an entry has a Python how-to and needs no key, it is run as published in an isolated sandbox (no secrets or environment variables, 60 s CPU, 90 s total, at most 25 connections to public addresses on web ports, 10 MB received), at most once a week per entry. It counts as OK when it produces a pandas DataFrame with rows. How-tos that need a key, stop at a limit, need a missing package or belong to a host whose `robots.txt` disallows automated requests are "not run" with the reason.

## Measured score (v2)
`score = round(100 × Σ wᵢ·cᵢ ÷ Σ wᵢ)` over the measured components only; each cᵢ is between 0 and 1, and a component that could not be measured is left out of both sums.

| Component | Weight | How it is measured |
|---|---|---|
| Uptime | 35 | Share of the last 30 checks answered with HTTP 2xx (skipped and blocked checks left out) |
| Freshness | 20 | Age of the newest measured change (see steps) |
| Licence clarity | 15 | 1 standard licence with published text (SPDX id); 0.5 provider's own terms with a terms link and reviewed note; 0.25 only one of the two; 0 unknown. Measures how clearly terms are stated, not how open they are |
| Auth friction | 15 | 1 no key or account; 0.75 none for part of the access; 0.5 free key, token or account; 0.25 on request or approval; 0 paid |
| How-to ran | 15 | 1 if the Python how-to produced a DataFrame with rows on the latest check, 0 if it failed; not measured when there is no how-to, it needs a key, or it stopped at a limit |

Freshness steps (days since newest measured change → value): ≤ 7 → 1, ≤ 31 → 0.8, ≤ 92 → 0.6, ≤ 366 → 0.4, ≤ 1096 → 0.2, older → 0.

An entry needs at least 3 daily checks before it gets a number; no score is estimated or carried over. The formula is versioned: a change in weights or steps gets a new version.

## Limits
One request a day shows a URL answered at that moment, not that every part of the service works. Last-Modified is the server's own claim. A provider page answering does not prove its data downloads work. Any other HTTP error or network failure counts as not reachable.

Questions or corrections: signal-lab@qdt.ai.
