# -*- coding: utf-8 -*-
"""Toorainete rasv ja süsivesikud (makrod), kirjutatud 8.11.2026.

Väärtused on 100 g (ml) kohta, munal tüki kohta, nagu ingredients.py kcal ja valk. Süsivesikud on nagu Eesti
pakendil: imenduvad süsivesikud ilma kiudaineteta. Allikad: USDA FoodData Central ja Fineli toitumistabelid,
valitud nii, et need sobivad toote kirjeldusega (piim 2,5%, hapukoor 20%, banaan koorega jne).

Kontroll: 4 x valk + 4 x süsivesikud + 9 x rasv peab olema kalorsuse lähedal (kiudained annavad juurde kuni
umbes 2 kcal grammi kohta, vein ka alkoholi). Kontroll käib iga käivitusega, kõrvalekalle peatab skripti.

Kasutus:
  python3 makrod.py          lisab fat ja carbs väljad äpi ingredients.json-isse (muud väljad jäävad samaks)
select_products.py kasutab sama tabelit, kui see ingredients.json uuesti kirjutab.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "..", "TaldrikCore", "Sources", "TaldrikCore", "Resources", "ingredients.json")

# id: (rasv, süsivesikud)
MACROS = {
    # küpsetamine, magus, pähklid (oma roogade jaoks)
    "mesi": (0, 81),
    "kakao": (21, 12),
    "sokolaad": (42, 34),
    "mandlijahu": (54, 9),
    "rosinad": (0.5, 70),
    "pahklid": (65, 7),
    "mandlid": (50, 9),
    "sarapuupahklid": (61, 7),
    "kupsetuspulber": (0, 25),
    "vanillisuhkur": (0, 99),
    "sooda": (0, 0),
    "kookoshelbed": (65, 7),
    "tarklis": (0.1, 86),
    "kondenspiim": (8.7, 54),
    "zelatiin": (0.1, 0),
    "datlid": (0.4, 67),
    "aprikoosid": (0.5, 55),
    "paevalilleseemned": (51, 11),
    "toorjuust": (24, 3.5),
    "kupsised": (21, 64),
    "lambaliha": (23, 0),
    "suitsuvorst": (29, 2),
    # liha
    "hakkliha": (20, 0),
    "kanafilee": (1.5, 0),
    "kanakoivad": (10.5, 0),
    "sealiha": (18, 0),
    "suitsuliha": (24, 0),
    "peekon": (38, 1),
    "viinerid": (22, 4),
    "kanahakkliha": (2, 0),
    "veisesteik": (15.5, 0),
    "veisehakkliha": (13.5, 0),
    "sisefilee": (4, 0),
    "sink": (3.5, 1.5),
    "pancetta": (43, 0.5),
    "seakarbonaad": (6, 0),
    "kanakintsuliha": (7, 0),
    "verivorst": (15, 20),
    "pardikoivad": (12.5, 0),
    "kanamaks": (4.8, 0.7),
    "searibid": (18.5, 0),
    "seakoot": (10.5, 0),
    # kala
    "kalafilee": (1, 0),
    "lohefilee": (13, 0),
    "kalapulgad": (9, 18),
    "tursafilee": (1, 0),
    "raim": (7.5, 0),
    "kilu": (14, 0.5),
    "heeringas": (16.5, 0.5),
    "tuunikala": (1, 0),
    "krevetid": (1, 0.5),
    "sinimerekarbid": (0.7, 1.2),
    # piim, munad
    "piim": (2.5, 4.7),
    "hapukoor": (20, 3.3),
    "koor": (16, 4),
    "void": (82, 0.7),
    "juust": (27.5, 0),
    "kohupiim": (5, 2.5),
    "jogurt": (3.5, 5.5),
    "munad": (5.5, 0.4),
    "kodujuust": (4.5, 2.5),
    "parmesan": (28, 0),
    "mozzarella": (19, 1.5),
    "sulajuust": (21, 5),
    "tofu": (8.5, 2),
    "pecorino": (28, 0),
    "keefir": (2.5, 4),
    "feta": (21.5, 1),
    "ricotta": (11, 3.5),
    # leib, kuivained
    "leib": (1.5, 44),
    "tortillad": (7, 50),
    "sai": (3.5, 48),
    "burgerisaiad": (5, 46),
    "riivsai": (4, 70),
    "kaerahelbed": (7, 59),
    "manna": (1, 71),
    "musli": (8, 64),
    "riis": (0.7, 78),
    "risotoriis": (0.7, 78),
    "pudruriis": (0.7, 78),
    "tatar": (3, 65),
    "pasta": (1.5, 71),
    "spagetid": (1.5, 71),
    "lasanje": (1.5, 71),
    "jahu": (1.2, 71),
    "odrakruubid": (1.2, 67),
    "herned": (1.5, 45),
    "laatsed": (2, 52),
    "nuudlid": (3, 69),
    "riisinuudlid": (0.6, 82),
    "kinoa": (6, 57),
    "kuskuss": (1, 72),
    "kama": (2.5, 63),
    "parm": (1.5, 8),
    "suhkur": (0, 100),
    "seesam": (50, 12),
    "maapahklid": (49.5, 13),
    "gnocchi": (0.4, 32),
    "lehttainas": (25, 38),
    # konservid, kastmed, õli
    "kikerherned": (1.5, 11),
    "punasedoad": (0.5, 13),
    "ubatomatis": (0.4, 12.5),
    "mais": (1.2, 14),
    "tomatipasta": (0.5, 18),
    "tomatid": (0.2, 4),
    "kookospiim": (18, 3),
    "sojakaste": (0, 6.5),
    "kalakaste": (0, 3.6),
    "ketsup": (0.2, 25),
    "majonees": (71, 2),
    "hapukurgid": (0.2, 2.5),
    "sriracha": (1, 19),
    "chilikaste": (0.2, 54),
    "moos": (0.1, 54),
    "pohlamoos": (0.2, 49),
    "oli": (92, 0),
    "oliivioli": (91, 0),
    "oliivid": (14, 1),
    "tahini": (54, 10),
    "pesto": (45, 5),
    "vein": (0, 2.6),
    "ananass": (0.1, 14.5),
    # külmutatud
    "herned_kulm": (0.4, 11.5),
    "kvsegu": (0.3, 6.5),
    "brokoli": (0.4, 4),
    "marjad": (0.4, 9),
    "edamame": (5.2, 5),
    "pelmeenid": (12, 28),
    # puu- ja köögiviljad
    "kartul": (0.1, 16),
    "porgand": (0.2, 7),
    "sibul": (0.1, 7.5),
    "kuuslauk": (0.5, 30),
    "kapsas": (0.1, 3.5),
    "hapukapsas": (0.1, 2.5),
    "peet": (0.2, 7),
    "kurk": (0.1, 3),
    "tomat": (0.2, 2.7),
    "paprika": (0.3, 5),
    "seened": (0.3, 0.5),
    "banaan": (0.2, 13.5),
    "oun": (0.2, 10.5),
    "sidrun": (0.3, 4),
    "laim": (0.2, 5),
    "spinat": (0.4, 1.4),
    "avokaado": (14.7, 1.8),
    "suvikorvits": (0.3, 2.1),
    "salat": (0.2, 1.5),
    "bataat": (0.1, 17),
    "till": (1.1, 4),
    "seller": (0.2, 1.5),
    "petersell": (0.8, 3),
    "basiilik": (0.6, 1),
    "koriander": (0.5, 0.9),
    "rohelinesibul": (0.2, 4.7),
    "ingver": (0.75, 15.8),
    "porrulauk": (0.3, 12.4),
    "kaalikas": (0.2, 6.5),
    # asendused (gluteeni- ja piimavaba)
    "gvpasta": (1.5, 78),
    "gvleib": (6, 42),
    "gvjahu": (1.5, 82),
    "gvkaer": (7, 59),
    "tamari": (0.1, 7),
    "gvtortillad": (5, 45),
    "kaerajook": (1.5, 6.5),
    "taimvoi": (57, 0.5),
    "kaerakoor": (13, 6),
    "taimjogurt": (2.3, 2.1),
    "taimjuust": (23, 18),
    "taimfraiche": (15, 6),
    "lillkapsas": (0.3, 3),
    "korvits": (0.1, 8.5),
}

# Lubatud kõrvalekalle kalorsusest: kiudained (kuni ~2 kcal grammi kohta) ja ümardused. Vein: alkohol.
NO_CHECK = {"vein"}


def check(ings):
    """Iga tooraine kohta: makrod olemas ja klapivad kalorsusega. Tagastab vigade loendi."""
    errors = []
    for x in ings:
        m = MACROS.get(x["id"])
        if m is None:
            errors.append(f"{x['id']}: rasv ja süsivesikud puuduvad (lisa MACROS-i)")
            continue
        fat, carbs = m
        prot = x.get("protein", x.get("prot"))
        if x["id"] in NO_CHECK:
            continue
        est = 4 * prot + 4 * carbs + 9 * fat
        kcal = x["kcal"]
        # kiudained lisavad köögiviljadel kuni ~25% (kapsas, seller), ümardused paar protsenti
        if est > kcal * 1.08 + 2 or est < kcal * 0.72 - 3:
            errors.append(f"{x['id']}: 4*{prot} + 4*{carbs} + 9*{fat} = {est:.0f} kcal, andmetes {kcal}")
    return errors


def main():
    ings = json.load(open(PATH, encoding="utf-8"))
    errors = check(ings)
    if errors:
        print("Makrod ei klapi:")
        for e in errors:
            print("  " + e)
        sys.exit(1)
    for x in ings:
        x["fat"], x["carbs"] = MACROS[x["id"]]
    json.dump(ings, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(ings)} toorainet, makrod lisatud")


if __name__ == "__main__":
    main()
