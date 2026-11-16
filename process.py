import csv, json, re, sys, io, os

src = sys.argv[1]
out = sys.argv[2]

groups = {}
route_list = []
route_idx = {}

def rid(name):
    if name not in route_idx:
        route_idx[name] = len(route_list)
        route_list.append(name)
    return route_idx[name]

TIER = {"Worker": 0, "Temporary Worker": 1}
RATING = {"A": 0, "B": 1, "": 2}

with io.open(src, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) < 5:
            continue
        name = row[0].strip()
        town = row[1].strip()
        county = row[2].strip()
        typ = row[3].strip()
        route = row[4].strip()
        if not name:
            continue
        m = re.search(r"\(\s*([AB])\s*rating\s*\)", typ, re.I)
        rating = m.group(1).upper() if m else ""
        tier = typ.split("(")[0].strip()
        tcode = TIER.get(tier, 0)
        rcode = RATING.get(rating, 2)
        key = (name.lower(), town.lower(), county.lower())
        if key not in groups:
            groups[key] = [name, town, county, []]
        groups[key][3].append([rid(route), tcode, rcode])

records = sorted(groups.values(), key=lambda x: x[0].lower())

payload = {
    "meta": {
        "source": "Home Office Register of licensed sponsors (Worker and Temporary Worker)",
        "register_date": "2026-11-12",
        "company_count": len(records),
    },
    "routes": route_list,
    "tiers": ["Worker", "Temporary Worker"],
    "ratings": ["A", "B", ""],
    "records": records,
}
json.dump(payload, open(out, "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))
print("companies:", len(records))
print("routes:", len(route_list))
print("json MB:", round(os.path.getsize(out) / 1048576, 2))
