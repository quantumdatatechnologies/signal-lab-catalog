#!/usr/bin/env python3
"""Regenerate data/catalog.json and data/catalog.csv from the public Signal Lab MCP server.

Standard library only. No authentication. Usage: python3 scripts/refresh.py
"""
import csv, json, os, sys, urllib.request

MCP_URL = "https://signal-lab.qdt.ai/api/mcp"
FIELDS = ["slug", "name", "providerUrl", "license", "licenseUrl", "licenseNote", "auth", "badge",
          "category", "domain", "type", "coverage", "freeTierLimits", "rateLimits", "docsUrl",
          "sitePageUrl", "tasks", "lastVerified", "attribution"]
# Output column names (id/url/licence are the friendly names for slug/providerUrl/license)
RENAME = {"slug": "id", "providerUrl": "url", "license": "licence", "licenseUrl": "licence_url",
          "licenseNote": "licence_note", "coverage": "description", "sitePageUrl": "signal_lab_url",
          "lastVerified": "last_verified", "freeTierLimits": "free_tier_limits",
          "rateLimits": "rate_limits", "docsUrl": "docs_url"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def call(name, arguments):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": name, "arguments": arguments}}).encode()
    req = urllib.request.Request(MCP_URL, body, {
        "content-type": "application/json", "accept": "application/json, text/event-stream",
        "user-agent": "signal-lab-open-refresh/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read().decode()
    payload = None
    for line in raw.splitlines():
        if line.startswith("data: "):
            payload = line[6:]
    msg = json.loads(payload or raw)
    if "error" in msg:
        sys.exit("MCP error: %s" % msg["error"])
    return json.loads(msg["result"]["content"][0]["text"])


def main():
    res = call("export_catalog", {"format": "json", "fields": FIELDS})
    entries = res["entries"]
    if len(entries) < 100 or len(entries) != res.get("matched", len(entries)):
        sys.exit("Unexpected export size: %d" % len(entries))
    rows = []
    for e in entries:
        row = {}
        for f in FIELDS:
            v = e.get(f, "")
            if isinstance(v, list):
                v = "; ".join(str(x) for x in v)
            row[RENAME.get(f, f)] = "" if v is None else v
        rows.append(row)
    rows.sort(key=lambda r: r["id"])
    os.makedirs(OUT, exist_ok=True)
    meta = {"source": MCP_URL, "tool": "export_catalog", "generated": res.get("generated"),
            "count": len(rows), "notice": res.get("notice"),
            "licence": "CC BY 4.0 for the compilation; each source keeps its own licence (see licence columns)"}
    with open(os.path.join(OUT, "catalog.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "entries": rows}, f, ensure_ascii=False, indent=1)
        f.write("\n")
    with open(os.path.join(OUT, "catalog.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("wrote %d entries (generated %s)" % (len(rows), res.get("generated")))


if __name__ == "__main__":
    main()
