# -*- coding: utf-8 -*-
"""Otsib iga tooraine otsingusõnad poodide e-poodidest ja salvestab vastused kausta data/raw.

Kasutus:
  python3 fetch.py            kõik poed
  python3 fetch.py rimi       üks pood
Päringute vahel on umbes 1 sekund poe kohta. Poode küsitakse paralleelselt.
"""
import json
import os
import sys
import threading
import time

from ingredients import I
from stores import FETCHERS, lidl_offers

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "data", "raw")
DELAY = 1.0


def queries():
    out = []
    for x in I:
        for q in x["q"]:
            if q not in out:
                out.append(q)
    return out


def run_store(store, qs, log):
    path = os.path.join(RAW, store + ".json")
    cache = {}
    if os.path.exists(path) and "--fresh" not in sys.argv:
        cache = json.load(open(path, encoding="utf-8"))
    fn = FETCHERS[store]
    todo = [q for q in qs if q not in cache]
    for n, q in enumerate(todo):
        t0 = time.time()
        try:
            cache[q] = fn(q)
        except Exception as e:
            log(f"{store}: '{q}' ebaõnnestus: {e}")
            continue
        if n % 10 == 0 or n == len(todo) - 1:
            log(f"{store}: {n + 1}/{len(todo)} '{q}' {len(cache[q])} toodet")
            json.dump(cache, open(path, "w", encoding="utf-8"), ensure_ascii=False)
        wait = DELAY - (time.time() - t0)
        if wait > 0:
            time.sleep(wait)
    json.dump(cache, open(path, "w", encoding="utf-8"), ensure_ascii=False)


def main():
    os.makedirs(RAW, exist_ok=True)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    stores = args or list(FETCHERS) + ["lidl"]
    lock = threading.Lock()

    def log(msg):
        with lock:
            print(msg, flush=True)

    qs = queries()
    log(f"{len(qs)} otsingut, poed: {', '.join(stores)}")
    threads = []
    for st in stores:
        if st == "lidl":
            continue
        th = threading.Thread(target=run_store, args=(st, qs, log))
        th.start()
        threads.append(th)
    if "lidl" in stores:
        offers = lidl_offers()
        json.dump(offers, open(os.path.join(RAW, "lidl.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        log(f"lidl: {len(offers)} täna kehtivat toidupakkumist")
    for th in threads:
        th.join()
    log("valmis")


if __name__ == "__main__":
    main()
