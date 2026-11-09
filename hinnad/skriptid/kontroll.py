# -*- coding: utf-8 -*-
"""Kontrollib uut hinnafaili enne avaldamist. Kui mõnest poest tuli järsku palju vähem tooteid (pood ei vastanud
või muutis lehte), jääb vana fail alles ja töö ebaõnnestub, nii et äpp ei saa poolikuid hindu.

Kasutus: python3 kontroll.py vana.json uus.json
"""
import json
import sys


def per_store(book):
    out = {}
    for row in book["items"].values():
        for st, prods in row.items():
            out[st] = out.get(st, 0) + len(prods)
    return out


old, new = (json.load(open(p, encoding="utf-8")) for p in sys.argv[1:3])
o, n = per_store(old), per_store(new)
# Lidli nädalapakkumiste arv käib üles ja alla, seda ei võrrelda
bad = ["%s: %d toodet, enne %d" % (st, n.get(st, 0), c) for st, c in o.items() if st != "lidl" and n.get(st, 0) < 0.7 * c]
if bad:
    sys.exit("Hinnad jäävad vanaks, sest mõnest poest tuli liiga vähe tooteid:\n  " + "\n  ".join(bad))
print("Korras: " + ", ".join("%s %d" % (st, c) for st, c in sorted(n.items())))
