#!/usr/bin/env python3
"""List tools, search the catalog and get one entry from the Signal Lab MCP server (stdlib only)."""
import json, urllib.request

URL = "https://signal-lab.qdt.ai/api/mcp"


def rpc(method, params=None, id=1):
    body = json.dumps({"jsonrpc": "2.0", "id": id, "method": method, "params": params or {}}).encode()
    req = urllib.request.Request(URL, body, {"content-type": "application/json",
                                             "accept": "application/json, text/event-stream"})
    raw = urllib.request.urlopen(req, timeout=60).read().decode()
    data = [l[6:] for l in raw.splitlines() if l.startswith("data: ")]
    msg = json.loads(data[-1] if data else raw)
    if "error" in msg:
        raise RuntimeError(msg["error"])
    return msg["result"]


def tool(name, **arguments):
    result = rpc("tools/call", {"name": name, "arguments": arguments})
    return json.loads(result["content"][0]["text"])


if __name__ == "__main__":
    tools = rpc("tools/list")["tools"]
    print("tools:", len(tools))
    found = tool("search_catalog", query="weather", limit=3)
    print(json.dumps(found, indent=1)[:600])
    rows = found.get("results") or found.get("entries") or found.get("rows") or []
    if rows:
        slug = rows[0]["slug"]
        entry = tool("get_entry", slug=slug)
        print("entry:", slug, "->", entry.get("name") or entry.get("entry", {}).get("name"))
