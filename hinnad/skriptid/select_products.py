# -*- coding: utf-8 -*-
"""Valib iga tooraine jaoks igast poest sobivad tooted ja kirjutab äpi andmed.

Iga poe kohta võetakse parima kilohinnaga toode ning lisaks üks väiksem ja üks suurem pakend
(pakendite kombineerimiseks). Kaalukaup on kilohinnaga. Hind on tavahind ilma kliendikaardita,
kampaaniahind ainult siis, kui see kehtib kõigile.

Kasutus:
  python3 select_products.py            kirjutab prices.json ja ingredients.json äpi sisse
  python3 select_products.py --table    prindib ka ülevaatetabeli
  python3 select_products.py --why kartul rimi   näitab, miks tooted välja jäid
  python3 select_products.py --only a,b --table  ainult need toorained: lisab või uuendab need olemasolevates
                                                 failides, teiste hinnad ja hinnafaili kuupäev jäävad samaks
"""
import json
import os
import re
import sys
from datetime import date

from ingredients import I

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "data", "raw")
# TALDRIK_OUT: kuhu kirjutada (GitHubi igapäevane töö kirjutab veebi kausta hinnad/)
OUT = os.environ.get("TALDRIK_OUT") or os.path.join(HERE, "..", "TaldrikCore", "Sources", "TaldrikCore", "Resources")
STORES = ["selver", "rimi", "barbora", "coop"]
SOURCE = {"selver": "Selver", "rimi": "Rimi", "barbora": "Barbora (Maxima)", "coop": "Coop",
          "lidl": "Lidli nädalapakkumised"}


def load():
    raw = {}
    for st in STORES:
        p = os.path.join(RAW, st + ".json")
        raw[st] = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    p = os.path.join(RAW, "lidl.json")
    lidl = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []
    return raw, lidl


SIZE_MULTI = re.compile(r"(\d+)\s*[x×]\s*(\d+(?:[.,]\d+)?)\s*(kg|g|gr|l|ml|cl|dl)\b", re.I)
SIZE_ONE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(kg|g|gr|l|ml|cl|dl)\b", re.I)
FACTOR = {"kg": 1000, "g": 1, "gr": 1, "l": 1000, "dl": 100, "cl": 10, "ml": 1}


def name_sizes(name):
    """Kõik nimes olevad suurused grammides (ml) järjekorras, nt "675g/385g" -> [675, 385]."""
    out, spans = [], []
    # "500/800,300g": suurusklass enne pakendit, mitte 800,3 g
    name = re.sub(r"(\d+/\d+),(\d)", r"\1, \2", name)
    for m in SIZE_MULTI.finditer(name):
        out.append((m.start(), int(m.group(1)) * float(m.group(2).replace(",", ".")) * FACTOR[m.group(3).lower()]))
        spans.append(m.span())
    for m in SIZE_ONE.finditer(name):
        if any(a <= m.start() < b for a, b in spans):
            continue
        out.append((m.start(), float(m.group(1).replace(",", ".")) * FACTOR[m.group(2).lower()]))
    return [z for _, z in sorted(out)]


def size_in_unit(p, ing):
    """Pakendi suurus tooraine ühikus või None, kui ei sobi.

    Kui nimes on mitu suurust (neto ja nõrutatud), võetakse neto. Purgis hapukurkidel nõrutatud kaal.
    """
    unit = ing["unit"]
    z, su = p.get("size"), p.get("sunit")
    # "550 g, ... 500 g neto": glasuuriga kaal ja neto, arvesta neto (nõrutatud toorainel jääb nõrutatud kaal)
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*(kg|g|gr|l|ml|cl|dl)\s*neto\b", p["name"], re.I)
    if m and unit != "tk" and not p.get("perpiece") and not ing.get("drained"):
        return float(m.group(1).replace(",", ".")) * FACTOR[m.group(2).lower()]
    if unit != "tk" and not p.get("perpiece") and su in ("g", "ml", None):
        sizes = name_sizes(p["name"])
        if sizes:
            z = min(sizes + ([z] if z else [])) if ing.get("drained") else sizes[0]
            su = su or "g"
    if p.get("perpiece"):
        return float(ing["piece"]) if ing.get("piece") and unit != "tk" else None
    if z is None:
        return None
    if unit == "tk":
        return z if su == "tk" else None
    if su in ("g", "ml"):
        return z
    if su == "tk" and ing.get("piece"):
        return z * ing["piece"]
    return None


def normalize(name):
    """Coop kirjutab š ja ž asemel sh ja zh ("Ketshup", "Shampinjonid", "tshilli")."""
    return (name.replace("sh", "š").replace("Sh", "Š").replace("SH", "Š")
            .replace("zh", "ž").replace("Zh", "Ž"))


def check(p, ing):
    """Tagastab (sobib, põhjus, suurus)."""
    name = normalize(p["name"])
    if re.match(r"haapsalu\b", name, re.I):
        return False, "Coop Haapsalu valmistoit", None
    for rx in ing["must"]:
        if not re.search(rx, name, re.I):
            return False, "puudub " + rx[:30], None
    if ing["ex"]:
        m = re.search(ing["ex"], name, re.I)
        if m:
            return False, "välistatud '" + m.group(0) + "'", None
    if p.get("price") is None or p["price"] <= 0:
        return False, "hind puudub", None
    if p.get("loose"):
        if not ing["loose"]:
            return False, "kaalukaup pole lubatud", None
        return True, "kaalukaup", None
    z = size_in_unit(p, ing)
    if z is None:
        return False, "pakendi suurus teadmata", None
    lo, hi = ing["size"]
    if not (lo <= z <= hi):
        return False, "pakend %g väljas vahemikust %g...%g" % (z, lo, hi), None
    return True, "", z


def unit_price(p, z):
    return p["price"] / 1000 if p.get("loose") else p["price"] / z


def choose(cands):
    """Parim ühikuhind + üks väiksem + üks suurem pakend."""
    if not cands:
        return []
    cands = sorted(cands, key=lambda c: (c[2], c[0]["name"]))
    best = cands[0]
    out = [best]
    if not best[0].get("loose"):
        bz = best[1]
        smaller = [c for c in cands if not c[0].get("loose") and c[1] < bz]
        bigger = [c for c in cands if not c[0].get("loose") and c[1] > bz]
        # väiksem pakend aitab väikese vajaduse korral, suurem siis, kui see pole palju kallim
        smaller = [c for c in smaller if c[2] <= best[2] * 3]
        bigger = [c for c in bigger if c[2] <= best[2] * 2]
        if smaller:
            out.append(min(smaller, key=lambda c: (c[2], -c[1])))
        if bigger:
            out.append(min(bigger, key=lambda c: (c[2], c[1])))
    return out


def as_app(p, z):
    return {
        "name": p["name"],
        "price": p["price"],
        "regular": max(p.get("regular") or p["price"], p["price"]),
        "size": None if p.get("loose") else z,
        "loose": bool(p.get("loose")),
        "url": p.get("url"),
        "perPiece": bool(p.get("perpiece")),
        "until": p.get("until"),
    }


def candidates_for(ing, products):
    seen = set()
    out = []
    for p in products:
        key = (p["name"], p.get("size"), p.get("price"))
        if key in seen:
            continue
        seen.add(key)
        ok, _, z = check(p, ing)
        if ok:
            out.append((p, z, unit_price(p, z)))
    return out


def per_kg_text(ing, up):
    if ing["unit"] == "tk":
        return "%.2f €/tk" % up
    return "%.2f €/%s" % (up * 1000, "l" if ing["unit"] == "ml" else "kg")


def main():
    only = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else set()
    unknown = only - {x["id"] for x in I}
    if unknown:
        sys.exit("Tundmatu tooraine: " + ", ".join(sorted(unknown)))
    raw, lidl = load()
    today = date.today()
    items = {}
    table = []
    for ing in I:
        row = {}
        for st in STORES:
            prods = [p for q in ing["q"] for p in raw[st].get(q, [])]
            picked = choose(candidates_for(ing, prods))
            row[st] = [as_app(p, z) for p, z, _ in picked]
            for p, z, up in picked:
                note = "KAMP" if p["price"] < (p.get("regular") or 0) - 0.005 else ""
                kg = p.get("kgprice")
                if kg and not p.get("loose") and ing["unit"] != "tk" and abs(p["price"] / z * 1000 - kg) / kg > 0.3:
                    note += " ?poe kilohind %.2f" % kg
                table.append((ing["id"], st, p["name"], "kaalukaup" if p.get("loose") else ("%g" % z),
                              p["price"], per_kg_text(ing, up), note))
            if not picked:
                table.append((ing["id"], st, "PUUDU", "", 0, "", ""))
        lp = choose(candidates_for(ing, lidl))
        if lp:
            row["lidl"] = [as_app(p, z) for p, z, _ in lp]
            for p, z, up in lp:
                table.append((ing["id"], "lidl", p["name"], "kaalukaup" if p.get("loose") else ("%g" % z),
                              p["price"], per_kg_text(ing, up), "kuni " + p["until"]))
        items[ing["id"]] = row
    count = sum(len(v) for r in items.values() for v in r.values())
    has_lidl = any("lidl" in r for r in items.values())
    srcs = [SOURCE[s] for s in STORES] + ([SOURCE["lidl"]] if has_lidl else [])
    book = {
        "date": today.isoformat(),
        "dateText": "%d.%d.%d" % (today.day, today.month, today.year),
        "sources": ", ".join(srcs[:-1]) + " ja " + srcs[-1],
        "items": items,
    }
    os.makedirs(OUT, exist_ok=True)
    ings = [{k: x[k] for k in ("id", "name", "unit", "section", "kcal", "pantry", "piece")} | {"protein": x["prot"]}
            for x in I]
    # rasv ja süsivesikud tabelist makrod.py (uuel toorainel peab see seal olemas olema)
    from makrod import MACROS, check
    errors = check(ings)
    if errors:
        sys.exit("Makrod ei klapi:\n  " + "\n  ".join(errors))
    for x in ings:
        x["fat"], x["carbs"] = MACROS[x["id"]]
    if only:
        # ainult valitud toorained olemasolevatesse failidesse (kuupäev ja teiste hinnad jäävad samaks)
        old_book = json.load(open(os.path.join(OUT, "prices.json"), encoding="utf-8"))
        for i in only:
            old_book["items"][i] = items[i]
        book = old_book
        old_ings = json.load(open(os.path.join(OUT, "ingredients.json"), encoding="utf-8"))
        by_id = {x["id"]: x for x in ings}
        known = {x["id"] for x in old_ings}
        old_ings = [by_id[x["id"]] if x["id"] in only else x for x in old_ings]
        old_ings += [x for x in ings if x["id"] in only and x["id"] not in known]
        ings = old_ings
        table = [t for t in table if t[0] in only]
        items = {i: items[i] for i in only}
        count = sum(len(v) for r in items.values() for v in r.values())
    json.dump(book, open(os.path.join(OUT, "prices.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(ings, open(os.path.join(OUT, "ingredients.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    missing = [(i, st) for i, r in items.items() for st in STORES if not r.get(st)]
    print("Kirjutatud: %d toodet, %d toorainet. Puudu: %s" % (count, len(items),
          ", ".join("%s@%s" % m for m in missing) or "mitte midagi"))
    if "--table" in sys.argv:
        w = max(len(t[2]) for t in table)
        cur = None
        for t in table:
            if t[0] != cur:
                print("\n" + t[0].upper())
                cur = t[0]
            print("  %-8s %-*s %9s %6.2f € %11s %s" % (t[1], min(w, 62), t[2][:62], t[3], t[4], t[5], t[6]))


def why(ing_id, store):
    raw, lidl = load()
    ing = next(x for x in I if x["id"] == ing_id)
    prods = lidl if store == "lidl" else [p for q in ing["q"] for p in raw[store].get(q, [])]
    seen = set()
    for p in prods:
        key = (p["name"], p.get("size"))
        if key in seen:
            continue
        seen.add(key)
        ok, reason, z = check(p, ing)
        print("%s %-60s %6s %s %s" % ("OK " if ok else "-- ", p["name"][:60], p["price"],
                                      "kaalukaup" if p.get("loose") else p.get("size"), reason))


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "--why":
        why(sys.argv[2], sys.argv[3])
    else:
        main()
