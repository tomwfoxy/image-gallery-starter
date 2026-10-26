"""Regenerate DATABASE.md and portfolio.csv from firms.json.

Run after every change to firms.json:  python3 pe-database/render.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).parent


def main():
    data = json.loads((ROOT / "firms.json").read_text())
    firms = sorted(data["firms"], key=lambda f: f["name"].lower())

    ids = [f["id"] for f in firms]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise SystemExit(f"Duplicate firm ids: {sorted(dupes)}")

    with open(ROOT / "portfolio.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["firm", "firm_hq", "typical_cheque", "company", "sector", "deal", "date", "status"])
        for f in firms:
            for p in f["portfolio"]:
                w.writerow([f["name"], f["hq"], f.get("typical_cheque", ""), p["name"],
                            p.get("sector", ""), p.get("deal", ""), p.get("date") or "", p["status"]])

    companies = sum(len(f["portfolio"]) for f in firms)
    lines = [
        "# UK Lower-Mid-Market Private Equity Database",
        "",
        f"_Generated from `firms.json` · last updated {data['meta']['last_updated']} · "
        f"{len(firms)} firms · {companies} portfolio companies_",
        "",
        f"**Scope:** {data['meta']['scope']}",
        "",
        "| Firm | HQ | Typical cheque | Sectors | Portfolio cos | Added |",
        "|---|---|---|---|---|---|",
    ]
    for f in firms:
        lines.append(f"| [{f['name']}](#{f['id']}) | {f['hq']} | {f.get('typical_cheque', '')} | "
                     f"{', '.join(f.get('sectors', []))} | {len(f['portfolio'])} | {f['added']} |")
    for f in firms:
        lines += ["", f"## {f['name']}", "", f"<a id=\"{f['id']}\"></a>", ""]
        lines.append(f"- **HQ / offices:** {f['hq']} ({', '.join(f.get('offices', []))})")
        lines.append(f"- **Website:** {f.get('website', '')}")
        lines.append(f"- **Strategy:** {f.get('strategy', '')}")
        if f.get("fund"):
            lines.append(f"- **Current fund:** {f['fund']}")
        if f.get("notes"):
            lines.append(f"- **Notes:** {f['notes']}")
        lines.append(f"- **Last checked:** {f['last_checked']}")
        lines += ["", "| Company | Sector | Deal | Date | Status |", "|---|---|---|---|---|"]
        for p in f["portfolio"]:
            lines.append(f"| {p['name']} | {p.get('sector', '')} | {p.get('deal', '')} | "
                         f"{p.get('date') or ''} | {p['status']} |")
        lines += ["", "Sources: " + " · ".join(f"<{s}>" for s in f.get("sources", []))]
    (ROOT / "DATABASE.md").write_text("\n".join(lines) + "\n")
    print(f"Rendered {len(firms)} firms, {companies} portfolio companies.")


if __name__ == "__main__":
    main()
