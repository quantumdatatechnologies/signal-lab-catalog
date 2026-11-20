// List tools, search the catalog and get one entry. Node 18+ (global fetch). Run: npx tsx mcp-example.ts
const URL_ = "https://signal-lab.qdt.ai/api/mcp";

async function rpc(method: string, params: object = {}) {
  const res = await fetch(URL_, {
    method: "POST",
    headers: { "content-type": "application/json", accept: "application/json, text/event-stream" },
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params }),
  });
  const raw = await res.text();
  const lines = raw.split("\n").filter((l) => l.startsWith("data: "));
  const msg = JSON.parse(lines.length ? lines[lines.length - 1].slice(6) : raw);
  if (msg.error) throw new Error(JSON.stringify(msg.error));
  return msg.result;
}

async function tool(name: string, args: object) {
  const r = await rpc("tools/call", { name, arguments: args });
  return JSON.parse(r.content[0].text);
}

const tools = (await rpc("tools/list")).tools;
console.log("tools:", tools.length);
const found = await tool("search_catalog", { query: "weather", limit: 3 });
const rows = found.results ?? found.entries ?? found.rows ?? [];
console.log(rows.map((r: any) => r.slug));
if (rows.length) {
  const entry = await tool("get_entry", { slug: rows[0].slug });
  console.log("entry:", rows[0].slug, "->", entry.name ?? entry.entry?.name);
}
