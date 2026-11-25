"""Check the ML Methods Library (ml-methods/) with the standard library only.

- every entry has the required fields, licence CC-BY-4.0, and 3 to 6 materials:
  1-2 papers, 1-2 implementations, exactly one tutorial and exactly one worked example
- every material has an https URL (or is marked no_open_link), a "why" note and a dated verification
- the computed scores (evidence, maturity, freshness) match their dated facts
- reviewed scores carry a reviewer, a date and a rationale
- index.json lists exactly the entries, with the same scores

Run: python3 scripts/check_ml_methods.py
"""
import datetime, glob, json, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ml-methods")
REQUIRED = json.load(open(os.path.join(ROOT, "schema.json")))["required"]
errors = []


def err(msg):
    errors.append(msg)


def evidence(e):
    doi = any(m["kind"] == "paper" and m.get("doi") for m in e["materials"])
    impl = any(m["kind"] == "implementation" and m.get("url") for m in e["materials"])
    return 1 + doi + impl + e["facts"]["benchmark_cited"] + e["facts"]["abstract_available"]


def maturity(e):
    c = e["facts"]["citations"]
    if not c:
        return None
    mx = max(x["cited_by"] for x in c)
    return 5 if mx >= 20000 else 4 if mx >= 5000 else 3 if mx >= 1000 else 2 if mx >= 200 else 1


def freshness(e):
    rs = e["facts"]["repos"]
    if not rs:
        return None
    day = lambda s: datetime.date.fromisoformat(s)
    ages = [10000 if r["archived"] else (day(r["checked"]) - day(r["last_push"])).days for r in rs]
    v = 5 if min(ages) <= 90 else 4 if min(ages) <= 365 else 3 if min(ages) <= 730 else 2
    return min(v, 4) if max(ages) > 365 else v


entries = {}
for path in sorted(glob.glob(os.path.join(ROOT, "entries", "*.json"))):
    e = json.load(open(path))
    name = os.path.basename(path)
    entries[e.get("id")] = e
    missing = [k for k in REQUIRED if k not in e]
    if missing:
        err(f"{name}: missing {missing}")
        continue
    if e["id"] + ".json" != name:
        err(f"{name}: id does not match file name")
    if e["license"] != "CC-BY-4.0":
        err(f"{name}: licence must be CC-BY-4.0")
    kinds = [m["kind"] for m in e["materials"]]
    if not (3 <= len(kinds) <= 6 and 1 <= kinds.count("paper") <= 2 and 1 <= kinds.count("implementation") <= 2
            and kinds.count("tutorial") == 1 and kinds.count("worked_example") == 1):
        err(f"{name}: materials mix {kinds}")
    for m in e["materials"]:
        if not m.get("why") or not m.get("verification", {}).get("checked"):
            err(f"{name}: {m['id']} needs a why note and a verification date")
        if m["url"] is None and m["verification"]["status"] != "no_open_link":
            err(f"{name}: {m['id']} has no URL")
        if m["url"] is not None and not m["url"].startswith("https://"):
            err(f"{name}: {m['id']} URL must be https")
    for k, fn in (("evidence", evidence), ("maturity", maturity), ("freshness", freshness)):
        if e["scores"][k]["value"] != fn(e) or e["scores"][k]["method"] != "code":
            err(f"{name}: computed {k} score does not match its facts")
    for k in ("theory", "ease", "fit"):
        s = e["scores"][k]
        if s["status"] == "reviewed" and not (s.get("reviewer") and s.get("reviewed") and len(s.get("rationale", "")) >= 10):
            err(f"{name}: reviewed {k} score needs reviewer, date and rationale")

index = json.load(open(os.path.join(ROOT, "index.json")))
ids = [m["id"] for m in index["methods"]]
if sorted(ids) != sorted(entries):
    err("index.json does not list exactly the entries")
for m in index["methods"]:
    e = entries.get(m["id"])
    if e and any(m["scores"][k] != e["scores"][k]["value"] for k in m["scores"]):
        err(f"index.json scores out of date for {m['id']}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"ml-methods: ok ({len(entries)} entries)")
