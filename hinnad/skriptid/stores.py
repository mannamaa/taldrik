# -*- coding: utf-8 -*-
"""Poodide e-poodide päringud ja vastuste ühtlustamine.

Iga pood annab tooted ühel kujul:
  name      toote nimi
  price     hind, mis kehtib kõigile (kampaania ilma kliendikaardita)
  regular   tavahind
  card      kliendikaardi hind (ainult info jaoks)
  size      pakendi suurus (g, ml või tk) või None
  sunit     suuruse ühik: g, ml, tk
  loose     True, kui hind on kilo või liitri kohta (kaalukaup)
  kgprice   poe teatatud hind kg või l kohta
  url       link poe lehele
  perpiece  True, kui müüakse tükikaupa ilma kaaluta (nt "Kurk, tk")
  until     Lidli pakkumise viimane päev (YYYY-MM-DD)
"""
import html
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
      "(KHTML, like Gecko) Version/18.0 Safari/605.1.15")
TALLINN = timezone(timedelta(hours=2))  # novembris EET


def http_get(url, accept="text/html,application/json;q=0.9,*/*;q=0.8", tries=3):
    last = None
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": accept,
                "Accept-Language": "et-EE,et;q=0.9,en;q=0.6",
            })
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # võrguviga, proovi uuesti
            last = e
            time.sleep(2 + 2 * k)
    raise last


def num(s):
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return float(s)
    s = str(s).strip().replace("\xa0", "").replace(" ", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


SIZE_MULTI = re.compile(r"(\d+)\s*[x×*]\s*(\d+(?:[.,]\d+)?)\s*(kg|g|gr|l|ml|cl|dl)\b", re.I)
SIZE_ONE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(kg|g|gr|l|ml|cl|dl)\b", re.I)
SIZE_PCS = re.compile(r"(\d+)\s*(tk|tükki|pcs)\b", re.I)


def to_base(amount, unit):
    u = unit.lower()
    if u == "kg":
        return amount * 1000, "g"
    if u in ("g", "gr"):
        return amount, "g"
    if u == "l":
        return amount * 1000, "ml"
    if u == "dl":
        return amount * 100, "ml"
    if u == "cl":
        return amount * 10, "ml"
    if u == "ml":
        return amount, "ml"
    return amount, u


def parse_size(text):
    """Leia nimest pakendi suurus. Tagastab (kogus, ühik) või (None, None)."""
    if not text:
        return None, None
    t = text.replace("\xa0", " ")
    m = list(SIZE_MULTI.finditer(t))
    if m:
        x = m[-1]
        a, u = to_base(num(x.group(2)), x.group(3))
        return int(x.group(1)) * a, u
    m = list(SIZE_ONE.finditer(t))
    if m:
        x = m[-1]
        return to_base(num(x.group(1)), x.group(2))
    m = list(SIZE_PCS.finditer(t))
    if m:
        return float(m[-1].group(1)), "tk"
    return None, None


def product(name, price, regular=None, card=None, size=None, sunit=None, loose=False,
            kgprice=None, url=None, perpiece=False, until=None, image=None):
    return {
        "name": re.sub(r"\s+", " ", html.unescape(name or "")).strip(),
        "price": round(price, 2) if price is not None else None,
        "regular": round(regular if regular is not None else price, 2) if price is not None else None,
        "card": round(card, 2) if card is not None else None,
        "size": size, "sunit": sunit, "loose": bool(loose),
        "kgprice": round(kgprice, 3) if kgprice else None,
        "url": url, "perpiece": bool(perpiece), "until": until,
        # väike tootepilt (ostunimekirja reale ja "Leia see pakk")
        "image": image,
    }


# ---------------------------------------------------------------- Selver
def selver(query):
    url = ("https://www.selver.ee/api/catalog/vue_storefront_catalog_et/product/_search?from=0&size=48&q="
           + urllib.parse.quote(query))
    d = json.loads(http_get(url, accept="application/json"))
    out = []
    for h in d.get("hits", {}).get("hits", []):
        s = h.get("_source", {})
        name = s.get("name") or ""
        if s.get("status") not in (1, "1", None):
            continue
        low = name.lower()
        if "ettetellimisel" in low or "selveri köök" in low:
            continue
        group = {p.get("customer_group_id"): p for p in s.get("prices", []) or []}
        g0 = group.get(0)
        if not g0:
            continue
        price = num(g0.get("final_price"))
        regular = num(g0.get("original_price")) or price
        cards = [num(group[g].get("final_price")) for g in (4, 7) if g in group]
        card = min(cards) if cards else None
        loose = bool(re.search(r",\s*kg\s*$", name, re.I))
        size, sunit = parse_size(s.get("product_volume") or "")
        if size is None:
            size, sunit = parse_size(name)
        perpiece = False
        if not loose and re.search(r",\s*tk\s*$", name, re.I) and (sunit in (None, "tk")) and (size in (None, 1.0)):
            perpiece, size, sunit = True, None, None
        img = s.get("thumbnail") or s.get("image")
        img = "https://www.selver.ee/img/200/200/resize" + img if isinstance(img, str) and img.startswith("/") else None
        out.append(product(name, price, regular, card, size, sunit, loose,
                           num(s.get("unit_price")), "https://www.selver.ee/" + (s.get("url_key") or ""),
                           perpiece, image=img))
    return out


# ---------------------------------------------------------------- Rimi
RIMI_PRICE = re.compile(r'class="price-tag card__price">\s*<span class="sr-only">\s*([\d.,]+)\s*€\s*per\s*(\w+)', re.S)
RIMI_OLD = re.compile(r"Tavahind:\s*([\d.,]+)\s*€")
RIMI_UNIT = re.compile(r"Hind ühiku kohta:\s*([\d.,]+)\s*€/(\w+)")
RIMI_HREF = re.compile(r'href="(/epood/ee/tooted/[^"]+)"')
RIMI_GTM = re.compile(r"data-gtm-eec-product='([^']*)'")
RIMI_IMG = re.compile(r'<img[^>]+src="(https://rimibaltic-res\.cloudinary\.com/[^"]+)"')


def rimi(query):
    url = "https://www.rimi.ee/epood/ee/otsing?query=" + urllib.parse.quote(query) + "&pageSize=80"
    t = http_get(url)
    out = []
    for part in t.split('<li class="product-grid__item"')[1:]:
        part = part[: part.find('<li class="product-grid__item"')] if '<li class="product-grid__item"' in part else part
        g = RIMI_GTM.search(part)
        if not g:
            continue
        try:
            gtm = json.loads(html.unescape(g.group(1)))
        except json.JSONDecodeError:
            continue
        name = gtm.get("name") or ""
        pm = RIMI_PRICE.search(part)
        if not pm:
            continue  # hinda pole (toode otsas)
        price = num(pm.group(1))
        per = pm.group(2).lower()
        old = RIMI_OLD.search(part)
        unit = RIMI_UNIT.search(part)
        kgprice = num(unit.group(1)) if unit else None
        href = RIMI_HREF.search(part)
        link = "https://www.rimi.ee" + href.group(1) if href else None
        regular = num(old.group(1)) if old else price
        im = RIMI_IMG.search(part)
        img = im.group(1).replace("w_auto", "w_200") if im else None
        if per == "kg":
            # kaalukaup: price on ühe umbkaudse tüki hind, õige kilohind on "Hind ühiku kohta"
            ratio = (regular / price) if price else 1.0
            out.append(product(name, kgprice, (kgprice or 0) * ratio, None, None, None, True,
                               kgprice, link, image=img))
            continue
        size, sunit = parse_size(name)
        perpiece = False
        if size is None and re.search(r"\btk\b", name, re.I):
            perpiece = True
        out.append(product(name, price, regular, None, size, sunit, False, kgprice, link, perpiece, image=img))
    return out


# ---------------------------------------------------------------- Barbora (Maxima)
def _walk_inventories(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "inventories" and isinstance(v, list):
                acc.extend(x for x in v if isinstance(x, dict))
            else:
                _walk_inventories(v, acc)
    elif isinstance(o, list):
        for v in o:
            _walk_inventories(v, acc)


def barbora(query):
    url = "https://barbora.ee/otsing?q=" + urllib.parse.quote(query)
    t = http_get(url)
    i = t.find("window.__remixContext = ")
    if i < 0:
        return []
    j = t.find(";</script>", i)
    ctx = json.loads(t[i + len("window.__remixContext = "):j])
    items = []
    _walk_inventories(ctx, items)
    out, seen = [], set()
    for it in items:
        if it.get("status") != "active":
            continue
        key = it.get("id")
        if key in seen:
            continue
        seen.add(key)
        name = it.get("title") or ""
        price = num(it.get("price"))
        promo = it.get("promotion") or None
        regular, card = price, None
        if promo and promo.get("oldPrice"):
            old = num(promo.get("oldPrice"))
            if promo.get("loyaltyCardRequired") or promo.get("mixAndMatch"):
                card, price, regular = price, old, old
            else:
                regular = old
        cu = it.get("comparativeUnit") or {}
        kgprice = num(cu.get("price"))
        loose = (it.get("unit") or {}).get("type") == "kg"
        link = "https://barbora.ee/p/" + (it.get("url") or "")
        img = it.get("image") if isinstance(it.get("image"), str) else None
        if loose:
            # Kaalukaubal on kilohind comparativeUnit.price, kampaania korral arvuta tavahinna suhe
            ratio = (regular / price) if price else 1.0
            if card is not None and promo and promo.get("oldPrice"):
                kg = kgprice * (num(promo.get("oldPrice")) / card) if card else kgprice
                out.append(product(name, kg, kg, kgprice, None, None, True, kg, link, image=img))
            else:
                out.append(product(name, kgprice, (kgprice or 0) * ratio, None, None, None, True, kgprice, link,
                                   image=img))
            continue
        size, sunit = parse_size(name)
        if size is None and kgprice and cu.get("type") in ("kg", "l") and price:
            size = round(price / kgprice * 1000)
            sunit = "g" if cu.get("type") == "kg" else "ml"
        perpiece = size is None and re.search(r"\btk\b", name, re.I) is not None
        out.append(product(name, price, regular, card, size, sunit, False, kgprice, link, perpiece, image=img))
    return out


# ---------------------------------------------------------------- Lidl
def lidl_offers(now=None):
    """Lidli veebis on ainult kehtivad ja tulevad nädalapakkumised. Võta täna kehtivad toidukaubad."""
    url = "https://www.lidl.ee/q/api/search?assortment=EE&locale=et_EE&version=v2.0.0&q=*&fetchsize=200"
    d = json.loads(http_get(url, accept="*/*"))
    now = now or time.time()
    out = []
    for it in d.get("items", []):
        g = (it.get("gridbox") or {}).get("data") or {}
        kf = g.get("keyfacts") or {}
        if "Toit" not in (kf.get("wonCategoryPrimary") or ""):
            continue
        until = None
        for b in (g.get("stockAvailability") or {}).get("badgeInfoV2") or []:
            vf, vu = b.get("validFrom"), b.get("validUntil")
            if vf and vu and vf <= now <= vu:
                until = datetime.fromtimestamp(vu, TALLINN).strftime("%Y-%m-%d")
        if not until:
            continue
        pr = g.get("price") or {}
        price = num(pr.get("price"))
        if price is None:
            continue
        regular = num(pr.get("oldPrice")) or price
        name = (g.get("fullTitle") or kf.get("fullTitle") or "").strip().lstrip("-\u2013\u2014 ").strip()
        pack = ((pr.get("packaging") or {}).get("text")) or ""
        desc = re.sub(r"<[^>]+>", " ", kf.get("description") or "")
        size, sunit = parse_size(pack)
        if size is None:
            size, sunit = parse_size(desc)
        if size is None:
            size, sunit = parse_size(name)
        base = ((pr.get("basePrice") or {}).get("text")) or ""
        kgprice = None
        m = re.search(r"1\s*(kg|l)\s*=\s*([\d.,]+)", base)
        if m:
            kgprice = num(m.group(2))
        loose = False
        if size is None and kgprice and abs(kgprice - price) < 0.005:
            loose = True
        link = "https://www.lidl.ee" + (g.get("canonicalUrl") or "")
        out.append(product(name, price, regular, None, size, sunit, loose, kgprice, link, False, until,
                           image=g.get("image") if isinstance(g.get("image"), str) else None))
    return out


# ---------------------------------------------------------------- Coop (Haapsalu e-pood, WooCommerce)
def coop_loose(name):
    """Kaalukaup: nimes on "kg" ilma arvuta ("Banaan kg", "Kurk kiles kg", "Kartul kg lahtine") või ligikaudne
    kaal ("Sea esikoot Rakvere ~1kg"): ligikaudse kaaluga liha ja kala hind on kilohind, mitte paki hind."""
    if re.search(r"~\s*\d", name):
        return True
    return (re.search(r"(^|\s)kg(\s|$)", name, re.I) is not None
            and re.search(r"\d\s*kg\b", name, re.I) is None)


# Kataloogi osad, kus toitu ei ole (lemmikloomad, alkohol, majapidamine, ettetellitavad vaagnad)
COOP_SKIP = re.compile(r"kassitoit|koeratoit|lemmikloom|lindude, näriliste|alkohol|õlu|siider|vein|viin\b|liköör|"
                       r"konjak|brändi|viski|rumm|dzinn|long drink|kokteil|hügieen|kosmeetika|deodorant|"
                       r"juuksehooldus|suuhooldus|kehahooldus|näohooldus|raseerimis|seebid|mähkmed|beebikaubad|"
                       r"kodutarbed|koristus|pesupesemis|nõudepesu|paberitooted|küünlad|hoidistamisvahend|"
                       r"apteegi|tervisetooted|vitamiin|garderoob|sokid|hooaja- ja vabaaja|aiakaubad|autokaubad|"
                       r"mänguasjad|matkatarbed|koolikaubad|kahjuritõrje|grillsöed|kinkepaber|kodutekstiil|"
                       r"tubaka|ajakirja|ettetellimisel|ettetellitavad|puhastusvahend|nahahooldus|deodorandid|pehme paber|"
                       r"patareid|spordikaubad|saunatarbed|rannatarbed|päevituskreem|lastetoidud", re.I)


def coop_item(it):
    if not it.get("is_in_stock") or not it.get("is_purchasable", True):
        return None
    name = html.unescape(it.get("name") or "")
    if re.match(r"haapsalu\b", name, re.I):
        return None  # Coop Haapsalu oma köögi valmistoidud ja pagaritooted
    pr = it.get("prices") or {}
    minor = int(pr.get("currency_minor_unit") or 2)
    try:
        price = int(pr.get("price")) / 10 ** minor
        regular = int(pr.get("regular_price") or pr.get("price")) / 10 ** minor
    except (TypeError, ValueError):
        return None
    loose = coop_loose(name)
    first = (it.get("images") or [{}])[0] if isinstance(it.get("images"), list) and it.get("images") else {}
    img = first.get("thumbnail") or first.get("src")
    if loose:
        return product(name, price, regular, None, None, None, True, price, it.get("permalink"), image=img)
    size, sunit = parse_size(name)
    perpiece = size is None and re.search(r"\btk\b", name, re.I) is not None
    kg = price / size * 1000 if size and sunit in ("g", "ml") else None
    return product(name, price, regular, None, size, sunit, False, kg, it.get("permalink"), perpiece, image=img)


COOP_API = "https://coophaapsalu.ee/wp-json/wc/store/v1/products?per_page=100"


def coop(query):
    """Coopil pole keskset e-poodi. Coop Haapsalu e-pood on piirkondlik, hinnad võivad teistes
    piirkondades erineda. Hinnad on sentides."""
    d = json.loads(http_get(COOP_API + "&search=" + urllib.parse.quote(query), accept="application/json"))
    return [p for p in map(coop_item, d if isinstance(d, list) else []) if p]


def coop_catalog(log=None, delay=0.3):
    """Kogu Coop Haapsalu e-poe toidukaup (umbes 100 lehte). Coopi otsing leiab ainult tooted, mille nimes on
    otsingusõna täpselt ("pangaasiuse filee" ei leia toodet "Pangasiusefilee"), nii et otsingusõnade kaupa jäi
    suur osa sobivaid tooteid leidmata. Kataloogist valib tooted tooraine filter (select_products.py)."""
    out, seen, page = [], set(), 1
    while True:
        d = json.loads(http_get(COOP_API + "&orderby=id&order=asc&page=%d" % page, accept="application/json"))
        if not isinstance(d, list) or not d:
            break
        for it in d:
            if it.get("id") in seen:
                continue
            seen.add(it.get("id"))
            if any(COOP_SKIP.search(c.get("name") or "") for c in it.get("categories") or []):
                continue
            p = coop_item(it)
            if p:
                out.append(p)
        if log and (page % 10 == 0):
            log("coop: kataloogi leht %d, %d toodet" % (page, len(out)))
        page += 1
        time.sleep(delay)
    return out


FETCHERS = {"selver": selver, "rimi": rimi, "barbora": barbora, "coop": coop}
