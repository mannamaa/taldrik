# -*- coding: utf-8 -*-
"""64 toorainet: toiteväärtus, poe osakond ja toote valiku filtrid.

Väljad:
  id, name    tooraine võti ja nimi äpis
  unit        g, ml või tk (tk ainult munadel)
  section     poe osakond: puu, leib, liha, kala, piim, kuiv, kons, kulm
  kcal, prot  100 g (ml) kohta, munal tüki kohta
  pantry      tavaliselt kodus olemas
  piece       ühe tüki kaal grammides, kui poes müüakse tükikaupa
  q           otsingusõnad
  must        regexid, mis kõik peavad nimes olema
  ex          välistav regex
  size        lubatud pakendi suurus (min, max) tooraine ühikus
  loose       kas kaalukaup on lubatud
  drained     arvesta nõrutatud kaalu (purgis hapukurgid)
"""

# Valmistoidud, mille nimes on tooraine. Kehtib enamikule toorainetele.
READY = (r"valmistoit|valmis|supp\b|supi\b|kaste\b|kastmes|salat\b|pirukas|pirukad|pelmeen|kotlet|pihv|burger|"
         r"rullis|vorm\b|hautis|praad\b|pitsa|pizza|lasanje kaste|krõps|chips|snäkk|snack|koera|kassi|lemmikl|"
         r"beebi|lapse|püree|smuuti|jook\b|joogi\b|mahl\b")

I = []


def ing(id, name, unit, section, kcal, prot, q, must, ex="", size=(0, 1e9), loose=True, pantry=False, piece=None,
        ready=True, drained=False):
    full_ex = "|".join(x for x in (ex, READY if ready else "") if x)
    I.append(dict(id=id, name=name, unit=unit, section=section, kcal=kcal, prot=prot, pantry=pantry, piece=piece,
                  q=q, must=must, ex=full_ex, size=size, loose=loose, drained=drained))


# ---------------------------------------------------------------- Liha
ing("hakkliha", "Hakkliha (sea-veise)", "g", "liha", 250, 17,
    ["hakkliha", "hakklihasegu", "seahakkliha"], [r"hakk"],
    r"kana|broiler|kalkun|lamba|ulukil|hirve|põdra|metssea|vegan|taim|soja|frikadell|kebab|maitsest|marin|"
    r"kotlet|täidis|külmutatud|grill|veise\s*hakk|veisehakk|^veise", (250, 1600))
ing("kanafilee", "Kana rinnafilee", "g", "liha", 110, 23,
    ["broileri rinnafilee", "kana rinnafilee", "rinnafilee"], [r"filee|filé", r"broiler|br\.|kana|rinna"],
    r"marin|maitsest|grill|suitsu|keedu|keedetud|sous|vide|kebab|vürts|paneer|nugget|šašlõk|šnitsel|minutipihv|"
    r"aasia|bbq|teriyaki|küpsetatud|praetud|ahjus|sink|vorst|kalkun|pardi|viil|tükid kastmes|lõhe|kala|sea|"
    r"veise|kõrvits|tikka|tandoori|pesto|mesi|sinep|küüslaugu|sidruni|ürdi|paprika|karri|toorjuust|juust|"
    r"chicken|kintsu|reie|koiv|tiiva|hakkliha|jogurt|mar\.", (300, 2600))
ing("kanakoivad", "Kanakoivad", "g", "liha", 150, 14,
    ["broileri koivad", "broileri poolkoivad", "kanakoivad", "broileri kintsud"],
    [r"broiler|br\.|kana|jah\.", r"koib|koiva|kintsu|reie|sääre|trummi|poolkoib"],
    r"marin|maitsest|grill|suitsu|bbq|filee|praetud|küpsetatud|kebab|vürts|ahju|keedu|keedetud|sous|šašlõk|"
    r"tiiva|kalkun|pardi|karri|mesi|sinep|küüslaugu|paprika|tikka|teriyaki|chili|tšilli|kana-|mar\.|"
    r"kintsuliha|kondita|ilma kondita|fileeritud", (400, 3200))
ing("sealiha", "Sealiha (kaela- või abaliha)", "g", "liha", 230, 17,
    ["sea kaelakarbonaad", "sea abatükk", "sealiha guljašš", "sea kaelaliha", "sea abaliha", "sealiha tükid"],
    [r"sea|sealiha", r"kaela|aba|guljašš|gulja|tükid|tükk|kuubik|abaliha|kaelaliha|praetükk|hautis"],
    r"marin|maitsest|grill|suitsu|šašlõk|bbq|hakk|sink|vorst|keedu|ribi|kõhu|pekk|peekon|sült|maks|neer|"
    r"süda|jalg|kõrv|saba|kont|praetud|küpsetatud|ahju|seljanka|herne|konserv|veise|lamba|kana|broiler|"
    r"kalkun|sous|vide|kebab|vürts|küüslaugu|sinep|mesi|karri|paprika|õlu|õlles|tšilli|chili|tikka|rull|"
    r"seakaela\s*viil|steik|kotlet|pihvid|šnitsel|šnitsl|pelmeen|klops|sibula", (300, 3200))
ing("suitsuliha", "Suitsuliha (ribi, koot, kont)", "g", "liha", 280, 15,
    ["suitsuribi", "suitsukoot", "suitsuliha", "suitsukont", "seljanka komplekt", "suitsutatud ribi"],
    [r"suitsu|suits\.|seljanka", r"ribi|koot|kont|liha|kintsu|seljanka|kaela|kõhu|supikogu"],
    r"hernes|herned|hallid|vorst|sink|peekon|viiner|juust|kala|lõhe|räim|forell|makrell|kana|broiler|kalkun|"
    r"pasteet|konserv|kapsas|mulgi|hautis|toorjuust|sea\s*ja\s*veise|veise|pardi|lamba|"
    r"seljanka(?!.*komplekt)|grill|kebab|krõbe|marin|maitsest|br\.|broil", (250, 2500))
ing("peekon", "Peekon", "g", "liha", 400, 13,
    ["peekon", "peekoni kuubikud"], [r"peekon(?!iga)"],
    r"maitse|juust|kana|kalkun|veise|praetud|kuivatatud|krõbe|munapuder|toorjuust|määre|pasteet|suupiste|"
    r"rullid|mähitud|mähis|ploomi|datli|seen|verivorst|vorst|focacc|sai\b|kaste|tom\.|amatriciana|marinaad",
    (100, 1100))
ing("viinerid", "Viinerid", "g", "liha", 260, 11,
    ["viinerid", "viiner"], [r"viiner"],
    r"veg|taim|soja|sai\b|leib|hot ?dog|kuivatatud|pasteet|mini\b|kokteil|kanaviiner(?!.*sea)", (200, 2200))

# ---------------------------------------------------------------- Kala ja külmutatud valmistooted
ing("kalafilee", "Valge kalafilee (külm.)", "g", "kulm", 80, 17,
    ["tursafilee", "heigifilee", "pangaasiuse filee", "kalafilee külmutatud", "pollocki filee", "alaska pollock"],
    [r"filee|filé|fileetük|tükid", r"tursk|tursa|heik|heigi|pangaas|pollock|merluus|tilaapia|tilapia|"
     r"kilttursk|saida|hoki|valge kala|kalafilee|meriahven|lest"],
    r"suitsu|soola|marin|paneer|riiv|pulgad|pulk|tomati|õli\b|õlis|konserv|vürts|praetud|keedu|lõhe|forell|"
    r"räim|kilu|makrell|vahemere|hõõrutud|ahju|grill|küüslaugu|sidruni|tilli|maitsest|tempura|batter|"
    r"taignas|krevet|segu|kalasupi|šnitsel|kotlet|kuubik|kartuli|juustu|spinati|brokoli|toorjuust|krõb|pan\.",
    (300, 2600))
ing("lohefilee", "Lõhefilee", "g", "kala", 200, 20,
    ["lõhefilee", "lõhe fileetükk", "lõhe portsjon"], [r"lõhe", r"filee|filé|fileetük|portsjon|tükk|tükid|selja"],
    r"suitsu|soola|marin|graav|kerge|viil|konserv|pasteet|määre|sushi|vürts|keedu|praetud|ahju|grill|sidruni|"
    r"tilli|maitsest|kõht|kõhu|uim|pea\b|kaaviar|mari\b|forell|teriyaki|pesto|ürdi|küüslaugu|toorjuust|"
    r"juust|spinati|kartuli|kreem|tatar|tartar|seljatükid\s*kastmes|hakk|kotlet|suflee", (200, 1600))
ing("kalapulgad", "Kalapulgad", "g", "kulm", 200, 12,
    ["kalapulgad"], [r"kalapulk|kalapulgad|fish fingers|kala\s*pulgad"],
    r"krabi|surimi|kalapulgakesed\s*juustu", (200, 1600))
ing("pelmeenid", "Pelmeenid", "g", "kulm", 260, 10,
    ["pelmeenid"], [r"pelmeen"],
    r"vegan|taim|kirsi|maasika|mustika|kohupiima|vareenik|kartuli|seene|kapsa|krevet|gyoza|dim ?sum|wonton|"
    r"pirukas|supp|kala|lõhe|juustu", (400, 2600), ready=False)

# ---------------------------------------------------------------- Piim ja munad
ing("piim", "Piim 2,5%", "ml", "piim", 52, 3.3,
    ["piim 2,5%", "piim 2.5%", "joogipiim"], [r"piim", r"2[,.]5\s*%"],
    r"laktoosivaba|šokolaadi|kakao|kohvi|mandli|kaera|soja|riisi|kookos|keefir|hapu|jogurt|pulber|"
    r"kondenseeritud|koor|vanilli|maasika|banaani|kokteil|petipiim|kitse|lõssi|piimajook|pakk\s*\d+x|"
    r"\d+\s*x\s*\d|kohupiim|juust", (500, 2100), loose=False, ready=False)
ing("hapukoor", "Hapukoor 20%", "g", "piim", 205, 2.6,
    ["hapukoor 20%", "hapukoor"], [r"hapukoor", r"20\s*%"],
    r"laktoosivaba|dip|maitse|küüslaugu|tilli|ürdi|jäätis|leib|kook|tort|kohuke|kiles|toorjuust|vegan|taim|"
    r"kaste|krõps|snäkk|kartuli|sibula", (150, 1100), loose=False, ready=False)
ing("koor", "Toiduvalmistamise koor", "ml", "piim", 170, 2.6,
    ["toiduvalmistamise koor", "kookimiskoor", "koor toiduvalmistamiseks", "rõõsk koor", "toiduvalmistamiskoor",
     "toidukoor"],
    [r"koor", r"toiduvalm|kooki|kokkami|rõõsk|kulinaar|kuumtöötl|cooking|toidukoor"],
    r"hapukoor|vahukoor|jäätis|kohvi|vegan|taim|kaera|soja|kookos|laktoosivaba|pulber|vanilli|šokol|"
    r"spray|sprei|vahusta|toorjuust|juustu", (150, 1100), loose=False)
ing("void", "Või", "g", "piim", 740, 0.6,
    ["või 82%", "või", "talu või"], [r"(^|[\s,])või\b"],
    r"võie|võileib|määre|margariin|toorjuust|maitse|küüslaugu|ürdi|sulatatud|ghee|kreem|kook|küpsis|sai\b|"
    r"croissant|kakao|šokolaadi|shea|kakaovõi|maapähkli|mandli|kookos|päevalille|taim|vegan|õli|seemne|"
    r"pähkli|kaste|mesi|leiva|praadimis|kartuli|pasta|riis|tatar|kalja|pannkoogi|puder|laktoosivaba|küüsl", (150, 600), loose=False)
ing("juust", "Juust (Eesti, Gouda, riivjuust)", "g", "piim", 350, 25,
    ["eesti juust", "gouda juust", "riivjuust", "juust viilutatud", "edam juust"],
    [r"(^|[\s,.])(riiv)?juust\b|\bgouda\b|\bedam\b"],
    r"toorjuust|sulatatud|kitse|lamba|mozzarella|parmesan|parmigiano|cheddar|brie|camembert|feta|halloumi|"
    r"mascarpone|maskarpone|ricotta|kodujuust|juustukook|saiake|vegan|taim|suitsu|vürtsi|küüslaugu|pähkli|"
    r"sinihallitus|hallitus|grana|emmental|maasdam|tilsit|juustupulgad|piimajook|kohupiim|leib|vorst|"
    r"viiner|kringel|kook|tort|juustukreem|määre|kreem|lõhna|tšilli|chili|pesto|ürdi|paprika|jalapeno|"
    r"tükkidena\s*õlis|õlis|marineeritud|pikantne|pipra|sibula|tomati|oliivi|trühvli|kimchi|kirsi|"
    r"juustuga|juustune|pannkoogi|pasta|mini\b|kuubikud\s*õlis|portsjon|grilli|leivakesed|krõbe|pulber|"
    r"prantsuse|hollandi\s*(?!gouda)|šveitsi|kreeka|itaalia|cheese(?!.*gouda)|lactose|laktoosivaba", (150, 1600), loose=False)
ing("kohupiim", "Kohupiim", "g", "piim", 120, 17,
    ["kohupiim"], [r"kohupiim"],
    r"kohuke|kreem|vanilli|rosina|maasika|šokolaadi|kakao|mee|marja|puuvilja|mustika|vaarika|kirsi|kook|"
    r"pirukas|sai\b|tort|pannkoo|sõrnik|laktoosivaba|magus|desert|vahu|toorjuust|kodujuust|keefir|jogurt|"
    r"taigna|määre|kaneeli|õuna|banaani|virsiku|aprikoosi|smuuti|pasha|ürdi|küüslaugu|pasta|ricotta", (180, 1100), loose=False)
ing("jogurt", "Maitsestamata jogurt", "g", "piim", 70, 4,
    ["maitsestamata jogurt", "naturaalne jogurt", "kreeka jogurt", "jogurt maitsestamata"],
    [r"jogurt", r"maitsestamata|naturaal|natural|kreeka|klassikaline|plain"],
    r"maasika|vanilli|virsiku|mustika|vaarika|kirsi|banaani|mango|šokolaadi|mee\b|marja|puuvilja|müsli|"
    r"joodav|laktoosivaba|vegan|taim|kaera|soja|kookos|kohuke|graanola|kreem|kook|jäätis|külmutatud|"
    r"suhkru|kirsi|ploomi|õuna|apelsini|sidruni|kaneeli|aprikoosi|karamelli|kohvi|jõhvika|pohla|astelpaju|"
    r"kirsi|rabarberi|granaatõuna|passion|pirni|kiivi|ananassi|kookos|pähkli|mandli|kurgi|ürdi|küüslaugu|"
    r"tzatziki|dip", (150, 1600), loose=False)
ing("munad", "Kanamunad", "tk", "piim", 80, 7,
    ["kanamunad", "munad"], [r"muna|munad|kanamuna"],
    r"munapuder|munasalat|munanuudl|nuudl|pasta|pulber|šokolaad|kinder|üllatus|pasha|lihavõtte|kunst|"
    r"dekor|vuti|keedetud|marineeritud|majonees|kook|sai\b|vahvl|liköör|šampoon|vedel|munavalge|"
    r"munakollane|kõva|kõvaks|munaga|munata|muna\s*ja|mozzarella|juustu", (4, 31), loose=False, ready=False)

# ---------------------------------------------------------------- Leib
ing("leib", "Rukkileib", "g", "leib", 230, 6,
    ["rukkileib", "leib viilutatud", "must leib"], [r"leib|rukki"],
    r"sai\b|röst|leivakesed|leivasnäkk|näkileib|näkk|kook|kringel|tort|kaneel|baguette|ciabatta|tortilla|"
    r"pita|lavash|leivavein|leivajook|kali|jahu|segu|juuretis|külmutatud|gluteenivaba|toast|hot ?dog|korp|"
    r"helbed|leivasupp|leivasupi|röstsai|röstleib|mini\b|kotletid|burger|vorm\b|pulgad|krutoon|juustu|"
    r"küüslaugu|seemne|seemnete|seemneleib|maisi|nisu|kaera|spelta|tatra|täistera\s*nisu|baltic|piima|"
    r"lahja|keeks", (300, 1300), loose=False)
ing("tortillad", "Tortillad", "g", "leib", 300, 8,
    ["tortilla", "tortillad", "tortilla wrap"], [r"tortilla|wrap|tortill"],
    r"krõps|chips|snäkk|nacho|salsa|maitseaine|komplekt|kit\b|taco|vorm\b|kana|veise|valmis|ümbris\s*valmis|"
    r"burrito\s*kit|pizza|pitsa|mini\b|täistera|rukki|spinati|tomati|gluteenivaba|maisi|mais|proteiin", (200, 1100),
    loose=False)

# ---------------------------------------------------------------- Kuivained
ing("riivsai", "Riivsai", "g", "kuiv", 360, 12,
    ["riivsai", "paneerimissegu"], [r"riivsai|paneerimis|panko"],
    r"maitsest|küüslaugu|ürdi|gluteenivaba|juustu|vürts|tšilli|krevet|riivsaias|paprika", (150, 1100), loose=False)
ing("kaerahelbed", "Kaerahelbed", "g", "kuiv", 370, 13,
    ["kaerahelbed"], [r"kaerahelb|kaera\s*helb"],
    r"küpsis|batoon|kiirpuder|maasika|mustika|vaarika|šokolaadi|kakao|vanilli|mee\b|puuvilja|marja|õuna|"
    r"kaneeli|banaani|rosina|graanola|müsli|gluteenivaba|kotike|portsjon|leib|sai\b|kliid|jahu|jook|"
    r"kreem|puder\s*\d|kaerapuder\s*(?!.*helbed)|organic|mahe", (400, 2100), loose=False)
ing("manna", "Manna", "g", "kuiv", 340, 11,
    ["mannatang", "manna"], [r"manna"],
    r"puder|kiir|maasika|vanilli|šokolaadi|kotike|portsjon|vaht|kook|desert|mannavaht|lapse|beebi|"
    r"täistera|kasha", (400, 2100), loose=False)
ing("musli", "Müsli", "g", "kuiv", 380, 9,
    ["müsli", "granola"], [r"müsli|granola|graanola"],
    r"batoon|baton|jogurt|kook|küpsis|kreem|kotike|portsjon|lapse|beebi|šokolaadi|šokolaad|kakao|"
    r"proteiin|valgu|keto|suhkruvaba|gluteenivaba", (300, 1600), loose=False)
ing("riis", "Riis", "g", "kuiv", 350, 7,
    ["riis", "pikateraline riis", "ümarateraline riis"], [r"riis"],
    r"riisipuder|puder|jahu|manna|nuudl|paber|vahvl|kook|piim|äädikas|keedu|keedetud|kotike|keedukot|portsjon|"
    r"risotto|sushi|metsik|pruun|täistera|must\b|punane|arborio|paella|mikro|pilaf|plov|maitsestatud|"
    r"köögivilja|galet|helbed|riisihelbed|kreem|vahvel|krõbe|kana|liha|karri|aurutatud\s*riis\s*\d+x|"
    r"\d+\s*x\s*\d+|kiirkeedu|kiir|riisijook|krõps", (400, 5100), loose=False)
ing("tatar", "Tatar", "g", "kuiv", 340, 12,
    ["tatar", "tatrakruup"], [r"tatar|tatra"],
    r"jahu|helbed|puder|nuudl|soba|keedukot|kotike|portsjon|leib|galet|pann|kook|tee\b|röstimata|roheline|"
    r"krõbe|hakkliha|liha|kana|seen|vorst|kiir", (400, 2100), loose=False)
ing("pasta", "Pasta (makaronid, fusilli)", "g", "kuiv", 355, 12,
    ["makaronid", "fusilli", "penne", "sarvekesed"],
    [r"makaron|fusilli|penne|sarvekes|torud|spiraal|pasta|farfalle|rigatoni|tigu|karbikes|liblik|sarved|"
     r"kõrred|tortiglioni|ditalini|maccheroni|elicoidali|gigli|conchiglie|caserecce|gemelli|cavatappi|"
     r"strozzapreti|orecchiette"],
    r"spaget|spaghet|lasanj|lasagn|tagliatelle|fettuccine|linguine|nuudl|pesto|toorjuust|juustu|kana|"
    r"täistera|gluteenivaba|munapasta|munaga|värske|täidetud|tortellini|ravioli|cannelloni|mini lasagn|"
    r"kuskuss|kinoa|riis|karri|külmutatud|tomati|basiiliku|spinati|rohelis|kikerherne|läätse|herne|tatra|"
    r"soja|tomatipasta|pastakaste|maitseaine|pastasegu|kiir|kõrvits|bolognese|carbonara|juustukaste|"
    r"pastaroog|hakkliha|tuunikala|kanaga|valgu|proteiin|mahe|bio\b|organic|lapsele|beebi|tähe|tähed|"
    r"loomakesed|vormid|kujud|supipasta|alfabet|vermicelli|orzo|risoni|pasta\s*salat|kastmes", (400, 3100),
    loose=False)
ing("spagetid", "Spagetid", "g", "kuiv", 355, 12,
    ["spagetid", "spaghetti"], [r"spaget|spaghet"],
    r"bolognese|carbonara|täistera|gluteenivaba|nuudl|riisi|kõrvits|mini\b|lapse|värske|spinati|munaga|"
    r"herne|läätse|kikerherne|tatra|soja|kiir|konserv|kastmes|juustu|tuunikala|kana|valgu|proteiin|"
    r"mahe|bio\b|organic|squash|kõrvitsa", (400, 3100), loose=False)
ing("lasanje", "Lasanjeplaadid", "g", "kuiv", 355, 12,
    ["lasanjeplaadid", "lasagne lehed", "lasanje lehed", "lasagne"],
    [r"lasanj|lasagn", r"plaadid|plaat|lehed|leht|sheets|sfoglie|lasagne\b|lasagna\b"],
    r"mini\b|valmis|külmutatud|bolognese|portsjon|kana|veise|köögivilja|vegan|taim|lasanjekaste|ahjus|"
    r"grill|hakkliha|lõhe|spinati|juustu|kotletid|bechamel|bešamel|sealiha|kalkun|lasanje\s*\d+\s*g$|"
    r"lasanje,\s*\d|külm\.|klassikaline\s*lasanje|lasanje\s*(?!plaadid|lehed).*\d+\s*g", (200, 1100),
    loose=False)
ing("jahu", "Nisujahu", "g", "kuiv", 340, 10,
    ["nisujahu"], [r"nisujahu|nisu\s*jahu"],
    r"täistera|segu|pannkoogi|pizza|pitsa|kook|sõõriku|gluteenivaba|spelta|durum|manitoba|\b00\b|kiir|"
    r"jahutatud|küpsetus|leiva|sai\b|isekerkiv|kerkiv|mahe|organic|bio\b", (900, 5100), loose=False,
    pantry=True)
ing("odrakruubid", "Odrakruubid", "g", "kuiv", 330, 9,
    ["odrakruubid", "kruubid", "odrakruup"], [r"kruup|kruubid"],
    r"helbed|jahu|puder|kotike|keedukot|portsjon|tang|tatra|kaera|riisi|nisu|mais|hirss|pärl|kiir",
    (400, 2100), loose=False)
ing("herned", "Kuivatatud herned", "g", "kuiv", 300, 22,
    ["kuivatatud herned", "herned poolitatud", "kollased herned", "hallid herned", "herned", "hernes"], [r"hern"],
    r"külmutatud|külm\.|roheline|rohelised|konserv|konserveeritud|purk|suhkru|aed|suitsu|sea|liha|wasabi|"
    r"kikerh|röstitud|pasta|nuudl|valk|proteiin|isolaat|jahu|maitsestatud|vürts|mais|oad|mung|"
    r"herneskaste|hernestega|hernesupp|krõbe|krõps|snäkk|segu|tükeldatud\s*liha|sealihaga|bonduelle|duopakk|helbed|ml\b", (400, 2100),
    loose=False, ready=False)
ing("laatsed", "Punased läätsed", "g", "kuiv", 340, 24,
    ["punased läätsed", "läätsed punased", "läätsed"], [r"lääts", r"punas|red\b"],
    r"konserv|purk|pasta|nuudl|jahu|krõps|snäkk|keedetud|eelkeedetud|kotike|keedukot|beluga|rohelised|"
    r"pruunid|mustad|supp|karri|dahl|daal|vürts|maitsest", (300, 2100), loose=False, ready=False)
ing("kikerherned", "Kikerherned (konserv)", "g", "kons", 85, 5,
    ["kikerherned konserv", "kikerherned"], [r"kikerhern"],
    r"kuivatatud|kuiv\b|jahu|pasta|krõps|snäkk|röstitud|hummus|valk|falafel|karri|vürts|maitsest|nuudl|"
    r"burger|tomati|tšilli|chili|oad|segu|mahe|bio\b|organic|krõbe|köögivilja|kikerhernestega", (200, 450), loose=False)
ing("nuudlid", "Supinuudlid", "g", "kuiv", 360, 13,
    ["supinuudlid", "munanuudlid", "vermišellid", "nuudlid"], [r"nuudl|vermišell|vermicelli|niidikesed|supipasta"],
    r"kiirnuudl|kiir|instant|maitsest|maitse|kana\s*maitse|karri|tassis|kauss|cup|wok|udon|soba|ramen|"
    r"riisi|klaas|tatra|täistera|gluteenivaba|tšilli|chili|veise|krevet|seene|köögivilja|liha|kana|vokin|magic|"
    r"miso|pho|pad thai|teriyaki|tom yum|kimchi|seesami|sojakastme", (150, 1100), loose=False)
ing("suhkur", "Suhkur", "g", "kuiv", 400, 0,
    ["suhkur"], [r"suhkur"],
    r"tuhksuhkur|tuhk|pruun|roosuhkur|vanilli|vaniljesuhkur|fariin|kookos|kaneeli|vahtra|siirup|asendaja|"
    r"stevia|magusti|suhkruvaba|tükk|tükisuhkur|kommi|vati|dekoor|geel|moos|hoidiste|želee|marmelaadi|"
    r"kook|küpsis|suhkruga|suhkrus|suhkrut|demerara|muscovado|kandis|candy|kristall\s*vanill|"
    r"suhkrupulber|suhkruhernes", (500, 3100), loose=False, pantry=True)

# ---------------------------------------------------------------- Konservid, kastmed, õli
ing("moos", "Moos", "g", "kons", 220, 0.4,
    ["moos", "maasikamoos", "vaarikamoos", "pohlamoos"], [r"moos|džemm|keedis"],
    r"suhkruvaba|kook|küpsis|jogurt|kohuke|pirukas|sai\b|vahvel|tort|rull|kreem|batoon|jäätis|chutney|"
    r"sibula|tšilli|chili|moosiga|kompvek|toorjuust|portsjon|kotike|sprei|siirup|kommi|šokolaadi|"
    r"pannkoogi|biskviit|leib|kohupiima|juustu|suhkur", (200, 1600), loose=False)
ing("oli", "Toiduõli (rapsi- või päevalilleõli)", "ml", "kons", 828, 0,
    ["rapsiõli", "päevalilleõli", "toiduõli"], [r"rapsiõli|päevalilleõli|taimeõli|toiduõli|rapsi|päevalille"],
    r"oliivi|seesami|kookos|linaseemne|kõrvitsa|pähkli|avokaado|sprei|spray|friteer|frittimis|maitsest|"
    r"küüslaugu|ürdi|tšilli|chili|majonees|margariin|seemned|seemne\b|kook|kala|kilu|sprot|tuunikala|"
    r"õlis|õliga|röstitud|kooritud|külmpress|mesi|kreem|või\b|määre|leib|sai\b|krõps|snäkk|halva",
    (450, 3100), loose=False, pantry=True)
ing("tomatipasta", "Tomatipasta", "g", "kons", 100, 4,
    ["tomatipasta", "tomatipüree"], [r"tomatipasta|tomatipüree|tomati\s*pasta|tomatikontsentraat|tomati\s*püree"],
    r"ketšup|basiiliku|küüslaugu|maitsest|päikesekuivatatud|passata|purustatud|tükeldatud|mahl|tuubis\s*ürdi|"
    r"ürdi|tšilli|chili|oliivi|pesto", (50, 600), loose=False, ready=False)
ing("tomatid", "Purustatud tomatid (konserv)", "g", "kons", 25, 1.2,
    ["purustatud tomatid", "tükeldatud tomatid", "tomatid omas mahlas", "kooritud tomatid"],
    [r"tomat", r"purustatud|tükeldatud|omas mahlas|hakitud|passata|kooritud|konserv|purk|tükid|tükkidena"],
    r"ketšup|basiiliku|küüslaugu|ürdi|tšilli|chili|pipra|oliivi|maitsest|päikesekuivatatud|kuivatatud|"
    r"tomatipasta|püree|salsa|kirss|kirsstomat|värske|karri|mozzarella|oregano|sibula|paprika|seene|"
    r"vürts|itaalia|provence|pesto|ürtidega|maitseainete|mahe|bio\b|organic", (300, 1100), loose=False)
ing("kookospiim", "Kookospiim", "ml", "kons", 180, 1.8,
    ["kookospiim", "kookosepiim", "kookosjook", "kookoskreem"], [r"kookos", r"piim|milk|kookosjook|kookoskreem|kookoskoor"],
    r"keha|šampoon|seep|losjoon|ihu|näo|kosmeet|dušš|palsam|deodorant|jäätis|jogurt|pulber|vahv|küpsis|"
    r"kommi|šokolaad|riis|puder|smuuti|batoon|kohv|latte|barista|kakao|"
    r"kookosvesi|vesi\b|vaht|geel|kliid|vahukoor|mandli|kaera|soja|banaani|maasika|alpro|helbed|õli\b|"
    r"joogiks|kreem\s*keha", (150, 600), loose=False, ready=False)
ing("sojakaste", "Sojakaste", "ml", "kons", 60, 8,
    ["sojakaste"], [r"sojakaste|soja\s*kaste|soy|shoyu|sojak"],
    r"teriyaki|magus|sweet|küüslaugu|tšilli|chili|ingveri|seente|marinaad|wok|nuudl|riis|kana|kalkun|"
    r"seesami|mesi|krõps|snäkk|tofu|piim|jogurt|joogi|jook|oad", (100, 1100), loose=False, ready=False)
ing("ketsup", "Ketšup", "g", "kons", 110, 1.5,
    ["ketšup", "ketchup", "ketshup"], [r"ketšup|ketchup|ketsup"],
    r"karri|curry|tšilli|chili|vürtsikas|hot\b|suhkruvaba|majonees|sinep|bbq|grill|šašlõki|"
    r"küüslaugu|mahe|bio\b|organic|lastele|mini\b|portsjon", (250, 1600), loose=False)
ing("majonees", "Majonees", "g", "kons", 650, 1,
    ["majonees"], [r"majonees|mayo"],
    r"küüslaugu|tšilli|chili|wasabi|trühvli|sriracha|vegan|taim|sinep|ketšup|dip|maitsestatud|tartar|"
    r"karri|curry|chipotle|ürdi|sidruni|munavaba|aioli|portsjon|mini\b", (200, 1100), loose=False)
ing("hapukurgid", "Hapukurgid", "g", "kons", 15, 0.5,
    ["hapukurgid", "marineeritud kurgid", "soolakurgid", "kornišonid", "marineeritud kurk", "hapukurk"],
    [r"kurgi?d|kurk|kornišon|kurgid", r"hapu|marine|soola|kornišon|äädika|äädikas"],
    r"värske|krõps|maitse|tartar|tzatziki|majonees|toorjuust|leib|sai\b|mahl|kurgisalat|salat|vürtsika|"
    r"tšilli|chili|mee|meega|sinepi|küüslaugu|tilli\s*kaste|kastme|kastmes|koor|hapukoor|viilud\s*võileiva",
    (250, 2100), loose=False, ready=False, drained=True)

# ---------------------------------------------------------------- Külmutatud
ing("herned_kulm", "Rohelised herned (külm.)", "g", "kulm", 80, 5,
    ["rohelised herned külmutatud", "külmutatud herned", "aedherned külmutatud", "herned", "hernes"],
    [r"hern", r"külm|külmutatud|sügavkülm|frozen"],
    r"konserv|purk|kuivatatud|suhkruhern|segu|köögiviljasegu|mais|porgand|wasabi|röstitud|kikerh|"
    r"lapse|beebi|sealiha|liha|riis|kartuli|oad|pasta|kaste|mahe|bio\b|organic|lumi|lumehern|"
    r"edamame|soja", (300, 2600), loose=False)
ing("kvsegu", "Köögiviljasegu (külm.)", "g", "kulm", 45, 2.5,
    ["köögiviljasegu külmutatud", "külmutatud köögiviljasegu", "köögiviljasegu", "wokisegu"],
    [r"segu|wok|mehhiko|hiina|talvine|suvine|kevadine|lečo|leečo|köögiviljad|juurviljad", r"külm|külmutatud|"
     r"sügavkülm|frozen|köögiviljasegu|wokisegu|wokiköögiviljad"],
    r"valmis|riisiga|kanaga|nuudlitega|pasta|lapse|beebi|smuuti|marja|puuvilja|friikartul|maitsestatud|"
    r"kartulisegu|ahju|grill|kastmega|kastmes|ürdi|vürts|marinaad|kanaliha|sealiha|krevet|kala|tofu|"
    r"riisi|kinoa|kuskuss|tatra|läätse|oa\b|oad|supisegu|supi|salatisegu|salati|seene|seened|kartuliga|"
    r"juustu|koore|vahemere|india|tai\b|teriyaki|sojakastme|vöö|mahe|bio\b|organic|lumi|"
    r"päevalille|pähkli|seemne|müsli|leiva|jahu|kuivatatud|pulber|mereand|krevet|kevadrull|rull|kartuli|coleslaw|borš", (300, 2600), loose=False)
ing("brokoli", "Brokoli (külm.)", "g", "kulm", 35, 3,
    ["brokoli külmutatud", "külmutatud brokoli", "brokoli"], [r"brok+ol|spargelkapsas"],
    r"segu|toit|lillkapsa|lillkapsas|porgandi|riisi|pasta|kartuli|juustu|gratään|sufl|lasanje|"
    r"kastmes|maitsestatud|mahe|bio\b|organic|püreesupp|koorene|võrsed|nuudl|mikro|salat", (300, 2600), loose=False)
ing("marjad", "Marjad (külm.)", "g", "kulm", 50, 0.7,
    ["külmutatud marjad", "marjasegu külmutatud", "külmutatud mustikad", "külmutatud maasikad",
     "külmutatud vaarikad", "mustikad", "maasikad", "marjad"],
    [r"mari|marja|mustika|maasika|vaarika|sõstra|pohla|jõhvika|murak|kirsi|astelpaju|aroonia|marjad|"
     r"mustikad|maasikad|vaarikad|sõstrad|pohlad|jõhvikad|kirsid", r"külm|külmutatud|sügavkülm|frozen"],
    r"jäätis|jogurt|kohuke|moos|kook|tort|pirukas|sorbet|šokolaad|kuivatatud|kompott|siirup|puder|müsli|"
    r"tee\b|kissell|kisell|vesi|morss|kreem|vaht|mahe|bio\b|organic|kooki|tarretis|desert", (200, 2600),
    loose=False)

# ---------------------------------------------------------------- Puu- ja köögiviljad
ing("kartul", "Kartul", "g", "puu", 77, 2,
    ["kartul", "kartulid", "kartul kg", "pestud kartul", "kartul võrgus"], [r"^(\S+\s+){0,2}kartul\b"],
    r"bataat|maguskartul|friikartul|fri\b|krõps|chips|püree|pudru|pulber|helbed|salat|pannkoo|kroket|ahju|"
    r"grill|maitsestatud|kooritud|külm|külmutatud|keedetud|varajane|uus\s*kartul|mini\b|beebi|"
    r"kartulijahu|tärklis|vorm\b|nuudl|gnocchi|röst|rösti|valmis|kotlet|pirukas|praetud|viil|viilud|sektor|"
    r"kuubik|kartuliroog|kaste|seemne|seemnekartul|vaakum|kartuliga|kartulite|kartulitega|kartulipuder|"
    r"lillkapsa|šampinjon|vorst|liha|kala|kana|kartulipirukas|kartulivorm|kartuli\s*\d|tükid|parmesani|"
    r"röstitud|grillitud|ürdi|küüslaugu|rosmariini|delikatess|lilla|punane|kollane\s*koor", (900, 10100))
ing("porgand", "Porgand", "g", "puu", 41, 0.9,
    ["porgand", "porgandid"], [r"^(\S+\s+)?porgand"],
    r"mahl|püree|salat|riivitud|kook|tort|pirukas|smuuti|krõps|snäkk|kuubik|viil|ribad|beebi|mini\b|"
    r"lapse|külm|külmutatud|segu|kaste|hapendatud|korea|marineeritud|kapsa|keedetud|kooritud|julienne|"
    r"pulgad|kotlet|burger|puder|moos|seemne|seemned|ingveri|õuna|porgandiga|herne|lilla|kollane|"
    r"punane|valge\s*porgand|mahe|bio\b|organic", (500, 5100))
ing("sibul", "Sibul", "g", "puu", 40, 1.1,
    ["sibul", "mugulsibul", "kuldne sibul"], [r"^(\S+\s+)?(mugul)?sibul\b"],
    r"punane|lilla|šalott|roheline|murulauk|porru|talisibul|kevad|marineeritud|praetud|krõbe|röstitud|"
    r"kuivatatud|pulber|helbed|graanul|chutney|moos|marmelaad|rõngad|kook|pirukas|leib|sai\b|maitse|vürts|"
    r"külm|külmutatud|hakitud|kuubik|seemne|seemned|küüslauk|ketšup|majonees|juust|toorjuust|sibulaga|"
    r"sibulatega|liha|vorst|kala|räim|heering|kilu|pärl|valge|mahe|bio\b|organic|kaste|krõps|snäkk|"
    r"hapukoore", (500, 5100))
ing("kuuslauk", "Küüslauk", "g", "puu", 150, 6,
    ["küüslauk"], [r"^küüslauk|^\s*küüslauk|^värske küüslauk|^küüslaugud"],
    r"pulber|graanul|helbed|kuivatatud|purustatud|hakitud|pasta|püree|marineeritud|õli\b|õlis|majonees|"
    r"leib|sai\b|maitse|vürts|sool|juust|toorjuust|või\b|kreem|kapsl|tablett|ekstrakt|siirup|tee\b|mesi|"
    r"röstitud|suitsu|must\s*küüslauk|metsküüslauk|karulauk|kooritud|mahe|bio\b|organic|seemne|kaste",
    (40, 600), piece=50)
ing("kapsas", "Valge peakapsas", "g", "puu", 25, 1.3,
    ["valge peakapsas", "peakapsas", "kapsas"], [r"^(\S+\s+)?(pea|valge)?kapsas\b"],
    r"hapu|lill|lillkapsas|punane|puna|savoy|kähar|hiina|pekingi|rooskapsas|brokoli|nui|nuikapsas|"
    r"lehtkapsas|kale|marineeritud|hautatud|rull|kapsarull|borš|seljanka|mulgi|hapendatud|kimchi|"
    r"sauerkraut|riivitud|tükeldatud|ribad|segu|külm|külmutatud|seemne|seemned|noor\s*kapsas|varajane|"
    r"mahe|bio\b|organic|kotlet|pirukas|porgandi", (500, 4100), piece=1000)
ing("hapukapsas", "Hapukapsas", "g", "puu", 20, 1,
    ["hapukapsas", "hapukapsad"], [r"hapukapsa|hapukapsas|hapendatud\s*kapsas"],
    r"hautatud|mulgi|liha|sea|vorst|kotlet|pirukas|valmis|pelmeen|vareenik|krõps|praetud|suitsu|"
    r"kartuli|salat|supp|pasta|kaste|mahe|bio\b|organic|jõhvika|pohla|õuna|ploomi|köömne|ürdi|marinaad|borš",
    (300, 3100), ready=False)
ing("peet", "Peet", "g", "puu", 43, 1.6,
    ["peet", "punapeet", "peet kg"], [r"^(punane\s+|söögi)?peet\b|^punapeet"],
    r"keedetud|aurutatud|marineeritud|salat|mahl|krõps|snäkk|püree|pulber|suhkru|lehed|beebi|mini\b|"
    r"kuubik|riivitud|viil|hapendatud|borš|supp|kaste|smuuti|vinegrett|rosolje|külm|külmutatud|valmis|"
    r"kooritud|vaakum|lehtpeet|söögipeet\s*keedetud|mahe|bio\b|organic|kaneeli|kitsejuustu|praetud|grill", (500, 5100))
ing("kurk", "Kurk", "g", "puu", 15, 0.7,
    ["kurk", "kurgid"], [r"^(\S+\s+)?kurk\b"],
    r"hapu|marine|soola|kornišon|äädika|salat|krõps|tzatziki|majonees|mahl|smuuti|vesi|limonaad|kosmeet|"
    r"mask|kreem|kurgiviil|mini\b|snäkk|beebi|seemne|seemned|merikurk|maitse|kastme|kurgi-|kurgisalat|marin|mar\.|"
    r"võileiva|pikniku|magus|salvest|"
    r"mahe|bio\b|organic|lühike|snack", (200, 2100), piece=300)
ing("tomat", "Tomat", "g", "puu", 18, 0.9,
    ["tomat", "tomatid"], [r"^(\S+\s+)?tomat(id)?\b"],
    r"kirss|kirsi|cherry|kaste|ketšup|pasta|püree|purustatud|tükeldatud|konserv|purk|omas mahlas|"
    r"päikesekuivatatud|kuivatatud|mahl|salsa|krõps|snäkk|maitse|basiiliku|pesto|passata|seemne|seemned|"
    r"istik|külm|mozzarella|kotlet|leib|sai\b|tomatiga|tomatites|tomatikaste|tomatipasta|tomatipüree|"
    r"keedetud|marineeritud|roheline|rohelised|kokteil|mini\b|snack|mahe|bio\b|organic|kobar|ploomtomat|"
    r"san marzano|lihatomat|beef|pärandsort|kollane|must|lilla|tomatisupp|tomatimahl", (250, 3100))
ing("paprika", "Paprika", "g", "puu", 30, 1,
    ["paprika", "punane paprika"], [r"^(\S+\s+)?paprika\b"],
    r"pulber|jahvatatud|suitsu|vürts|maitse|krõps|chips|snäkk|kaste|pasta|püree|marineeritud|grillitud|"
    r"röstitud|konserv|purk|õlis|täidetud|salat|mini\b|seemne|seemned|ajvar|lecso|lečo|leečo|kotlet|"
    r"vorst|juust|toorjuust|hummus|leib|sai\b|külmutatud|külm|ribad|kuubik|segu|tšilli|chili|jalapeno|"
    r"pepperoni|terav|snack|mahe|bio\b|organic|paprikaga|paprikaga|paprikakaste|paprikaliha|"
    r"pikk\s*paprika|magus\s*pikk|kreeka|kirss", (150, 2100), piece=180)
ing("seened", "Šampinjonid", "g", "puu", 22, 3,
    ["šampinjonid", "sampinjonid", "shampinjonid", "shampinjon"], [r"^(\S+\s+)?(šampinjon|sampinjon|champignon)"],
    r"konserv|purk|marineeritud|püree|kuivatatud|pulber|külm|külmutatud|praetud|pasteet|pirukas|"
    r"toorjuust|juust|valmis|seenesegu|segu|portobello|kuninga|osteri|šiitake|kukeseen|puravik|"
    r"metsaseen|viilutatud\s*konserv|tervena\s*konserv|kastmes|koorese|mahe|bio\b|organic|soolvees|vees\b|marin|"
    r"seenekaste|vürts", (200, 2100))
ing("banaan", "Banaan", "g", "puu", 60, 0.8,
    ["banaan", "banaanid"], [r"^(\S+\s+)?banaan"],
    r"krõps|kuivatatud|chips|snäkk|jogurt|smuuti|püree|kook|leib|sai\b|batoon|kohuke|jäätis|šokolaad|mahl|"
    r"pulber|beebi|lapse|vahv|kreem|liköör|maitse|minibanaan|baby|mini\b|keedubanaan|plantain|plaatan|"
    r"roheline|punane|mahe|bio\b|organic|fairtrade\s*mini", (500, 3100))
ing("oun", "Õun", "g", "puu", 48, 0.3,
    ["õun", "õunad"], [r"^õun(ad)?\b"],
    r"mahl|püree|kuivatatud|krõps|chips|snäkk|kook|pirukas|strudel|moos|kompott|siider|äädikas|smuuti|"
    r"jook|tee\b|vesi|kaste|jogurt|kohuke|batoon|leib|sai\b|pulber|beebi|lapse|šokolaad|karamell|kaneel|"
    r"sorbet|jäätis|maitse|aroom|õunaga|õuna\s*ja|õunte|seemne|granaatõun|maaõun|kaneeli|mini\b|"
    r"mahe|bio\b|organic|siidri|veini|šampoon|seep", (500, 3100))
ing("sidrun", "Sidrun", "g", "puu", 25, 0.5,
    ["sidrun", "sidrunid"], [r"^sidrun(id)?\b"],
    r"mahl|kontsentraat|maitse|sidruniga|sidrunimaitseline|tee\b|vesi|limonaad|jook|siirup|kook|tort|"
    r"pirukas|küpsis|kreem|jogurt|kohuke|sool|pipar|kala|kana|marinaad|kastme|kaste|koor\b|riivitud|"
    r"kuivatatud|hape|sidrunhape|pulber|moos|marmelaad|curd|sorbet|jäätis|kommi|kompvek|šokolaad|seep|"
    r"nõudepesu|puhastus|lõhna|õhuvärsk|käte|kosmeet|leib|sai\b|muffin|koogike|lime|laim|mahe|bio\b|"
    r"organic|meyer", (100, 1600), piece=120)

# ---------------------------------------------------------------- Fit-retseptide toorained (lisatud 7.11.2026)
ing("kanahakkliha", "Kanahakkliha", "g", "liha", 110, 22,
    ["kanahakkliha", "broileri hakkliha", "kana hakkliha", "broilerihakkliha"],
    [r"hakk", r"kana|broiler|br\.|rinnafilee"],
    r"kalkun|sea|veise|kotlet|maitsest|marin|pallid|frikadell|kebab|pihv|lamba|külmutatud", (250, 1100))
ing("kodujuust", "Kodujuust", "g", "piim", 100, 12,
    ["kodujuust"], [r"kodujuust|cottage"],
    r"kodujuustu|ürdi|küüslaugu|maitse|ananassi|maasika|vaarika|virsiku|kurgi|tilli|paprika|laktoosivaba|kreem|"
    r"pirukas|kook|sai\b|pannkoogi|lõhe|sink|mee\b|meega|kirsi|mango|marja|puuvilja|mustika|sõstra|astelpaju|"
    r"pirni|õuna|banaani|šokolaadi|vanilli", (150, 1100), loose=False)
ing("tuunikala", "Tuunikala omas mahlas", "g", "kons", 110, 25,
    ["tuunikala omas mahlas", "tuunikala konserv", "tuunikala"], [r"tuunikala|tuun\b"],
    r"õlis|õliga|salat|pasta|tomati|pasteet|määre|sushi|steik|külm|maitsest|tšilli|chili|sidruni|ürdi|"
    r"oliivi|vürts|kreem|tikud|köögivilja|mais|oad|riis|kaste|kastmes|pipra|toit\b|kiisu|kassi|kass\b|sheba|"
    r"gourmet|perle|furrito|whiskas|felix|koera|lemmik|tortilla|tasku|tuunikalaga|kauss", (80, 450), loose=False,
    ready=False, drained=True)
ing("bataat", "Bataat", "g", "puu", 86, 1.6,
    ["bataat", "maguskartul"], [r"bataat|maguskartul"],
    r"krõps|friikartul|fri\b|püree|külm|külmutatud|kuivatatud|chips|snäkk|pulber|jahu|mini\b|beebi|lapse|"
    r"kotlet|salat|supp|mahe|bio\b|organic", (300, 3100), piece=400)
ing("kinoa", "Kinoa", "g", "kuiv", 368, 14,
    ["kinoa", "quinoa"], [r"kinoa|quinoa"],
    r"salat|valmis|keedetud|kotike|keedukot|helbed|jahu|krõps|snäkk|pasta|batoon|segu|riis|bulgur|kuskuss|"
    r"maitsest|köögivilja|portsjon|mikro|paisutatud|puffed|krõbe|kana|mahe|bio\b|organic|müsli|kreeker|kauss|"
    r"kinoaga|tomatiga|päikese|\bPT\b|\bGN\b|vaarika|datli|chia|galet|makar", (250, 1100),
    loose=False)
ing("spinat", "Spinat (värske)", "g", "puu", 23, 2.9,
    ["spinat", "beebispinat", "värske spinat"], [r"spinat"],
    r"külm|sügavkülm|hakitud|portsjonid|härmavili|potis|kreem|koore|pasta|pesto|juust|pirukas|lasanje|smuuti|"
    r"supp|kaste|seemne|seemned|segu|rukola|kotlet|tortilla|wrap|leib|sai\b|ravioli|ravioolid|tortellini|"
    r"omlett|krõps|pulber|mini\b|mahe|bio\b|eco\b|organic|kartuli|riisi|kana|lõhe|pannkoo|püree|pür\.|"
    r"\d+\s*k\b|\d\+|kringel|stritsel|müsli|koera|kassi|filotaig|võileib", (60, 1100), ready=False)
ing("avokaado", "Avokaado", "g", "puu", 160, 2,
    ["avokaado"], [r"^(\S+\s+)?avokaado"],
    r"guacamole|kaste|dip|õli|krõps|kreem|mask|kosmeet|pasta|määre|salat|külm|külmutatud|kuubik|püree|sushi|"
    r"smuuti|mini\b|šampoon|seep|näo|toit\b|mahe|bio\b|organic|leib|wrap|hummus|avokaadoga", (140, 1600),
    piece=170,
    ready=False)
ing("suvikorvits", "Suvikõrvits", "g", "puu", 17, 1.2,
    ["suvikõrvits"], [r"suvikõrvits"],
    r"külm|külmutatud|grill|marineeritud|pasta|nuudl|spiraal|spagett|lasanje|kotlet|pannkoo|salat|supp|"
    r"püree|krõps|seemne|pirukas|vorm\b|kreem|leib|sai\b|mini\b|beebi|lapse|mahe|bio\b|organic", (200, 2100),
    piece=300)
ing("salat", "Lehtsalat", "g", "puu", 15, 1.2,
    ["rooma salat", "jääsalat", "lehtsalat"],
    [r"^(\S+\s+)?(rooma\s*salat|jääsalat|lehtsalat|aedsalat|romaine|salat\s*(rooma|jää|lehe|lollo|romaine))"],
    r"kaste|kastmega|kana|tuunikala|kartuli|pasta|kapsa|kurgi|tomati|peedi|porgandi|singi|lõhe|krevet|"
    r"valmis|mix|segu|seemne|krutoon|grill|caesar|kreeka|mini\b|mahe|bio\b|organic|seeme", (100, 1100),
    piece=300, ready=False)

# ---------------------------------------------------------------- Pidulikumad road (lisatud 7.11.2026)
ing("veisesteik", "Veise antrekoot või ribeye", "g", "liha", 220, 20,
    ["veise antrekoot", "antrekoot", "ribeye", "veise välisfilee", "veise steik"],
    [r"antrekoot|ribeye|rib\s*eye|entrecote|välisfilee|striploin|steik"],
    r"sea|kana|broiler|kalkun|lamba|hirve|põdra|metssea|marin|maitsest|kaste|burger|hakk|külmutatud|kuivat|"
    r"jerky|suitsu|vorst|sink|lõhe|kala|tuun|vegan|taim|soja|pihv|kotlet|šnitsel|portobello|seene|kapsa|"
    r"sous|vide|vürts|küüslaugu|pipra|ürdi|bbq|wagyu|kuivlaagerdatud\s*\d+\s*päeva", (150, 2600))
ing("veisehakkliha", "Veisehakkliha", "g", "liha", 200, 19,
    ["veisehakkliha", "veise hakkliha"], [r"veise\s*-?\s*hakk|veisehakk"],
    r"sea|kana|broiler|kalkun|lamba|kotlet|burger|pihv|frikadell|marin|maitsest|külmutatud|kebab|täidis|vegan|"
    r"taim|soja|segu|lihapall|pelmeen|kaste|bolognese", (250, 1600))
ing("krevetid", "Krevetid (kooritud, külmutatud)", "g", "kulm", 70, 15,
    ["kooritud krevetid", "krevetid", "tiigrikrevetid"], [r"^(\S+\.?\s+){0,2}(tiigri|tiiger|kuning)?krevet"],
    r"koorega|koores|koorimata|\bkoor\.|terve|peaga|sabaga|sabad|pan\.|riivsai|juust|oliiv|moiva|kalamarj|kreeker|"
    r"krevettidega|s\.vees|"
    r"salat|kaste|kastmes|tempura|paneer|batter|sushi|marin|küüslaugu|tšilli|chili|"
    r"vürts|maitsest|soolvee|kokteil|kreem|vorm|pasta|riis|wok|supp|krõps|snäkk|pulber|pasteet|määre|kook|"
    r"spring|rull|dim\s*sum|gyoza|wonton|vegan|taim|imitatsioon|surimi|krabi|tikk|vardas", (150, 1600),
    loose=False)
ing("sisefilee", "Sea sisefilee", "g", "liha", 120, 21,
    ["sea sisefilee", "sisefilee"], [r"sisefilee|sisefilé"],
    r"veise|kana|broiler|kalkun|lamba|hirve|põdra|marin|maitsest|grill|küüslaugu|ürdi|pipra|mee\b|mesi|sinepi|"
    r"peekon|sink|suitsu|vorst|sous|vide|bbq|vürts|paprika|karri|kaste|kastmes|täidetud|täidis|rull|külmutatud",
    (250, 2100))
ing("parmesan", "Parmesan või Grana Padano", "g", "piim", 390, 33,
    ["parmesan", "grana padano", "parmigiano reggiano"], [r"parmesan|parmigiano|grana\s*padano"],
    r"kaste|pesto|krõps|kreeker|küpsis|maitse|vegan|taim|pasta|ravioli|tortellini|risotto|salat|leib|sai\b|"
    r"pulber|kook|pirukas|vorst|sink|kreem|määre|sulatatud|snäkk|chips|pulgad|jerky|sticks|broiler|lihast|cigar",
    (60, 1100))
ing("burgerisaiad", "Burgerisaiad", "g", "leib", 270, 9,
    ["burgerikukkel", "burgerisaiad", "hamburgerisaiad", "burgeri saiad"], [r"burger|hamburger"],
    r"pihv|kotlet|liha|kana|veise|sea\b|juust|vegan|taim|kaste|ketsup|kurgi|komplekt|kit\b|mini\b|"
    r"gluteenivaba|valmis|kalkuni|lõhe|kala|kartuli|retroburger|mamma\b", (150, 1100), loose=False, piece=75,
    ready=False)
ing("risotoriis", "Risotoriis (Arborio)", "g", "kuiv", 350, 7,
    ["risotoriis", "arborio riis", "risotto riis"], [r"risot|arborio|carnaroli"],
    r"valmis|seene|seentega|juustu|kana|maitse|kaste|pulber|mix|segu|köögivilja|spargli|kõrvitsa|tomati|"
    r"krevet|mereand|safran|portsjon|mikro|kiir", (300, 1100), loose=False)

# ---------------------------------------------------------------- Rohkem kodutoite (lisatud 7.11.2026)
ing("sink", "Sink (viilutatud)", "g", "liha", 110, 18,
    ["sink", "keedusink", "viilutatud sink", "singiviilud"], [r"(^|\s)(keedu|ahju|toore|hiina)?sink\b|singivii"],
    r"suitsusink|toorsink|prosciutto|serrano|parma|jamon|kana|kalkun|broiler|vorst|pasteet|juust|salat|pitsa|pizza|"
    r"võileib|wrap|pirukas|rull|tortilla|kaste|veise|lõhe|kala|vegan|taim|soja|sarvesai|saiake|kook|krõps|munaga|"
    r"tükid kastmes|kartuli|pasta|makaron", (80, 1100))
ing("mozzarella", "Mozzarella", "g", "piim", 250, 18,
    ["mozzarella", "riivitud mozzarella", "mozzarella juust"], [r"mozzarella"],
    r"pulgad|snäkk|pitsa|pizza|salat|paneer|tomati|pesto|vegan|taim|burrata|mini\b|kuulikesed|pallikesed|"
    r"pärlid|cherry|ürdi|küüslaugu|tšilli|chili|leib|sai\b|wrap|lasanje|pan\.|pannkoog|vorst|külmutatud",
    (100, 1100))
ing("parm", "Pärm", "g", "kuiv", 100, 12,
    ["pärm", "kuivpärm", "värske pärm"], [r"pärm"],
    r"toitu|pärmitaigen|tainas|taigen|sai\b|saiake|kook|pirukas|leib|helbed|maitse|ekstrakt|vitamiin|õlu|siider|"
    r"kringel|stritsel|pulber\s*küpset|küpsetuspulber|jahusegu|pärmivaba|ciabatta|lehttaig|pärmi-", (5, 600),
    ready=False)
ing("sulajuust", "Sulatatud juust", "g", "piim", 260, 12,
    ["sulatatud juust", "sulajuust"], [r"sulatatud\s*juust|sulajuust|sul\.\s*juust"],
    r"kreveti|seene|singi|vorsti|peekoni|ürdi|tilli|paprika|tšilli|chili|krabi|lõhe|kala|kana|viilud|viil\b|"
    r"kolmnurk|batoon|kreeker|šokolaadi|vanilli|mini\b|pulgad|sibula|juustu-|küüslaugu|tomati|oliivi|trühvli|"
    r"maitseline|vorst|grill", (100, 800))

# ---------------------------------------------------------------- Poke-kausid (7.11.2026)
ing("sriracha", "Sriracha-tšillikaste", "ml", "kons", 100, 2,
    ["sriracha", "sriracha kaste"], [r"sriracha"],
    r"majonees|mayo|krõps|snäkk|pähkl|nuudl|chips|kana|tofu|ketšup|ketchup|mini\b|portsjon|sool\b|maitseaine|"
    r"seemned|hummus|juust|vorst|popkorn|surimi|pulgad|kastmega|krabi|majo|broiler|rinnafilee|ribad",
    (50, 1000), loose=False, ready=False)
ing("chilikaste", "Magus tšillikaste", "ml", "kons", 220, 0.5,
    ["magus tšillikaste", "sweet chili kaste", "sweet chilli", "magus tšilli"],
    [r"(magus|sweet).{0,14}(tšilli|chil)|(tšilli|chil).{0,8}magus"],
    r"krõps|snäkk|pähkl|nuudl|chips|kana|kreveti|tofu|majonees|mayo|mini\b|portsjon|marinaad|juust|vorst|"
    r"popkorn|kartul|pulgad|seemned|hummus|dip\b|ketšup|ketchup|toorjuust|ingveri",
    (100, 1000), loose=False, ready=False)
ing("seesam", "Seesamiseemned", "g", "kuiv", 570, 18,
    ["seesamiseemned", "seesam"], [r"seesam"],
    r"õli|pasta|tahini|leib|sai\b|kreeker|batoon|küpsis|halvaa|kaste|kastmega|kana|krõps|snäkk|bagel|kukkel|"
    r"pulgad|segu|müsli|helbed|batoonid|kommi|šokolaad|maitseaine|juust|baton|leivake|näkileib|riisikook|"
    r"seemnetega|seesamiga|filo|toru|tainas|feta|rõngik|bagel|sai\b|saiake|näkileiv|crisp|-ga\b|maiuspulk|"
    r"vitakraft|viirpap|papagoi|lind",
    (50, 600), loose=False)
ing("tofu", "Tofu", "g", "piim", 140, 14,
    ["tofu", "naturaalne tofu", "tofu naturaalne"], [r"tofu"],
    r"suitsu|marin|maitsestatud|maitsega|pulgad|pihv|burger|vorst|nuudl|supp|kaste|jogurt|magustoit|siid|silken|"
    r"praetud|tšilli|chili|karri|curry|küüslaugu|ürdi|basiiliku|krõbe|snäkk|mini\b|pasta|salat|toit\b|joogi|jook|"
    r"köömne|kroket|pasteet|puder|tilli|magus|sibula|määre|vahu|kreem|kassi|liiv|batoon|glasuur|morinaga|mori-nu",
    (150, 1100), loose=False)
ing("edamame", "Edamame-sojaoad (külm.)", "g", "kulm", 120, 11,
    ["edamame", "edamame oad", "sojaoad külmutatud"], [r"edamame|sojaoa|soja\s*oa"],
    r"kaunas|kaunades|kaunad|snäkk|krõps|röstitud|soolatud|nuudl|segu|salat|kaste|wok|pasta|kuivatatud|konserv|"
    r"jook|joogi|piim|jogurt|tofu|vorst|burger|pihv",
    (200, 1100), loose=False)
ing("mais", "Mais (konserv)", "g", "kons", 80, 2.5,
    ["mais konserv", "suhkrumais", "maisiterad"], [r"mais"],
    r"popkorn|pop\s*corn|krõps|helbed|jahu|tärklis|pudru|tortilla|nacho|küpsis|leib|kolb|tõlvik|külmutatud|"
    r"segu|köögiviljasegu|mehhiko|salat|beebi|mini|õli|snäkk|maisipulgad|pulgad|kana|kalkun|toit\b|tšilli|chili|"
    r"oad|herned|porgand|paprika|kreem|supp|mahe|bio\b|organic|maisiterad\s*ja|poolik|vaakum|keedu|keedetud|"
    r"tõlvik|kolvid|grill|tangud|kruup|polenta|manna|klaaspurk",
    (140, 600), loose=False, drained=True)

# ---------------------------------------------------------------- Klassikalised road (7.11.2026)
ing("pancetta", "Pancetta või guanciale", "g", "liha", 450, 14,
    ["pancetta", "guanciale", "pancetta kuubikud"], [r"pancetta|guanciale"],
    r"pitsa|pizza|salat|kaste|wrap|võileib|mini\b|snäkk|krõps|pasta\b|pasteet|vorst|juust|kana|kalkun|"
    r"kreeker|leib|sai\b|rull\b|maitsest|suitsut",
    (60, 600), loose=False)
ing("pecorino", "Pecorino Romano", "g", "piim", 390, 32,
    ["pecorino romano", "pecorino"], [r"pecorino"],
    r"vein|\bvv\b|0[.,]75|\bbio\b|kaste|pesto|kreeker|pasta\b|salat|leib|sai\b|krõps|snäkk|ravioli|tortelli",
    (80, 600), loose=False)

# ---------------------------------------------------------------- Retseptide parandused, 1. partii (7.11.2026)
ing("till", "Till (värske)", "g", "puu", 43, 3.5,
    ["till", "värske till", "till kimp"], [r"(^|\s)till(\s|,|$)|^tilli"],
    r"kurk|kurgi|kartul|kaste|soola|marin|seemne|kuivatatud|kuiv\b|külm|külmutatud|tilliga|tilli-|juust|leib|krõps|"
    r"vorst|heeringas|kala|salat|kreem|dip|maitse|õli|sool\b|vürts|hakitud|kotanyi|pesto|tillipesto|santa maria",
    (10, 300), loose=False)
ing("seller", "Varsseller", "g", "puu", 16, 0.7,
    ["varsseller", "seller"], [r"seller"],
    r"juur|mugul|salat|mahl|smuuti|soola|sool\b|kuivatatud|maitse|supp|segu|pulgad|dip|krõps|püree|külm",
    (100, 1000))
ing("oliivid", "Oliivid (kivideta)", "g", "kons", 140, 1,
    ["oliivid kivideta", "mustad oliivid", "rohelised oliivid"], [r"oliiv"],
    r"õli|pasta|tapenaad|määre|leib|sai\b|krõps|täidisega|täidetud|anšoov|küüslaugu|tšilli|chili|marinaad|segu|salat|"
    r"pitsa|kreem|dip|kividega|kivid\b|seep|kosmeet|majonees|provansaal",
    (100, 1000), loose=False, drained=True)

# ---------------------------------------------------------------- Uued klassikud ja retseptide 2. partii (7.11.2026)
# Värsked ürdid
ing("petersell", "Petersell (värske)", "g", "puu", 36, 3.0,
    ["petersell", "lehtpetersell", "värske petersell"], [r"^(\S+\s+)?(leht)?petersell\b"],
    r"juur|kuivatatud|kuiv\b|külm|külmutatud|seemne|maitse|pesto|õli|sool\b|vürts|hakitud|kotanyi|santa maria|"
    r"kaste|dip|juust|leib|krõps|salat|segu|või\b|küüslaugu|puljong|krutoon", (10, 300), loose=False, piece=30)
ing("basiilik", "Basiilik (värske)", "g", "puu", 23, 3.2,
    ["basiilik", "värske basiilik"], [r"^(\S+\s+)?basiilik\b"],
    r"kuivatatud|kuiv\b|külm|külmutatud|pesto|õli|kaste|maitse|sool\b|vürts|kotanyi|santa maria|tomati|juust|"
    r"mozzarella|seemne|tee\b|segu|leib|krõps|pasta|dip|kreem|siirup|jook|limonaad|äädik|hakitud|tofu|vahvl|sink",
    (10, 300), loose=False, piece=25)
ing("koriander", "Koriander (värske)", "g", "puu", 23, 2.1,
    ["koriander", "värske koriander"], [r"^(\S+\s+)?koriander\b"],
    r"seemne|seemned|jahvatatud|kuivatatud|kuiv\b|terve\b|külm|külmutatud|maitse|vürts|kotanyi|santa maria|kaste|"
    r"pasta|õli|leib|sool\b|segu|tee\b|hakitud|pesto|dip|geel|kreem|seep|šampoon", (10, 300), loose=False, piece=25)
ing("rohelinesibul", "Roheline sibul", "g", "puu", 32, 1.8,
    ["roheline sibul", "sibulapealsed", "kevadsibul"],
    [r"roheline\s*sibul|rohelised\s*sibulad|sibulapeal|sibula\s*pealsed|kevadsibul"],
    r"kuivatatud|kuiv\b|külm|külmutatud|krõps|chips|snäkk|kaste|dip|juust|toorjuust|maitse|vürts|segu|leib|"
    r"sool\b|pesto|kreem|hapukoor|salat|pirukas|pelmeen|kotlet|vorst|seemne|leivakr|koore-", (30, 600), loose=False,
    piece=100)
# Juurviljad ja puuviljad
ing("ingver", "Ingver (värske juur)", "g", "puu", 80, 1.8,
    ["ingver", "ingverijuur", "värske ingver"], [r"ingver"],
    r"jahvatatud|kuivatatud|kuiv\b|marineeritud|marin|sushi|pasta|püree|tee\b|jook|shot|šott|mahl|limonaad|siirup|"
    r"kommi|kompvek|šokolaad|küpsis|piparkook|kook|õlu|ale\b|kaste|maitse|vürts|kotanyi|santa maria|suhkru|"
    r"glasuur|kristall|pulber|sidruni|mee\b|mesi|kurkum|smuuti|kapsul|ekstrakt|riivitud|kombucha|vesi|kurgi|"
    r"porgandi|õuna|apelsini|ingveriga|mahe|bio\b|organic|suši|šot\b|roosa|jõhvika", (30, 1100), piece=60)
ing("laim", "Laim", "g", "puu", 30, 0.7,
    ["laim", "laimid"], [r"^laim(id)?\b|^lime\b"],
    r"mahl|kontsentraat|maitse|tee\b|vesi|limonaad|jook|siirup|kook|tort|kreem|jogurt|kohuke|sool\b|pipar|"
    r"marinaad|kaste|lehed|kaffir|kuivatatud|pulber|curd|jäätis|kommi|šokolaad|seep|nõudepesu|puhastus|lõhna|"
    r"õhuvärsk|käte|mahe|bio\b|organic|piparmündi|mojito", (60, 1600), piece=65)
ing("porrulauk", "Porrulauk", "g", "puu", 61, 1.5,
    ["porrulauk", "porru"], [r"porru"],
    r"külm|külmutatud|kuivatatud|supp|segu|pirukas|salat|krõps|püree|kreem|seemne|juust|kaste|mahe|bio\b|organic",
    (150, 2100), piece=250)
ing("kaalikas", "Kaalikas", "g", "puu", 37, 1.1,
    ["kaalikas", "kaalikad"], [r"kaalik"],
    r"püree|krõps|külm|külmutatud|supp|salat|segu|kuubik|hakitud|lapse|beebi|seemne|mahe|bio\b|organic",
    (300, 3100), piece=800)
# Liha ja kala
ing("seakarbonaad", "Sea välisfilee (karbonaad)", "g", "liha", 140, 21,
    ["sea välisfilee", "seakarbonaad", "sea karbonaad", "karbonaad"],
    [r"välisfilee|karbonaad|seljatükk|seljaliha", r"sea|välisfilee|karbonaad"],
    r"kaela|veise|kana|broiler|kalkun|lamba|marin|maitsest|grill|suitsu|šašlõk|bbq|paneer|šnitsel|šnitsl|keedu|"
    r"praetud|küpsetatud|ahju|kotlet|vürts|küüslaugu|sinepi|mee\b|mesi|karri|paprika|kastmes|sous|vide|sink|"
    r"vorst|rull|täidetud|kondiga|luuga|kotlett|pihv|külmutatud|kebab|ürdi|pipra|kamaraga", (300, 2600))
ing("kanakintsuliha", "Kana kintsuliha (kondita)", "g", "liha", 140, 19,
    ["broileri kintsuliha", "kana kintsuliha", "broileri kintsufilee", "kana reiefilee", "kintsuliha"],
    [r"broiler|br\.|kana|jah\.|kintsuliha", r"kintsuliha|kintsufilee|reiefilee|reieliha|kondita\s*kints|"
     r"fileeritud\s*kints|kintsu\s*filee|reie\s*filee|kints\w*\s*kondita"],
    r"marin|maitsest|grill|suitsu|bbq|praetud|küpsetatud|kebab|vürts|ahju|keedu|keedetud|sous|šašlõk|kalkun|"
    r"pardi|karri|mesi|sinep|küüslaugu|paprika|tikka|teriyaki|chili|tšilli|mar\.|hakk|kotlet|kondiga|ürdi|"
    r"pipra|külmutatud|gyros|šašlõ|juust|suits|steik|~", (300, 2600))
ing("verivorst", "Verivorst", "g", "liha", 260, 11,
    ["verivorst", "verivorstid"], [r"verivorst"],
    r"leib|pirukas|sai\b|kaste|pasteet|valmis|toit\b|kartuli|kapsa|mini\b|kokteil|vegan|taim|viilutatud",
    (300, 2600))
ing("tursafilee", "Tursafilee (külm.)", "g", "kulm", 82, 18,
    ["tursafilee", "tursk filee", "tursa fileetükid"], [r"tursa|tursk", r"filee|filé|fileetük|seljatük|portsjon|tükid"],
    r"suitsu|soola|marin|paneer|riiv|pulgad|pulk|tomati|õli\b|õlis|konserv|vürts|praetud|keedu|lõhe|forell|räim|"
    r"kilu|makrell|vahemere|hõõrutud|ahju|grill|küüslaugu|sidruni|tilli|maitsest|tempura|batter|taignas|krevet|"
    r"segu|kalasupi|šnitsel|kotlet|kuubik|kartuli|juustu|spinati|brokoli|toorjuust|krõb|pan\.|maks|mari\b|"
    r"kaaviar|kilttursk|kilttursa|saida|alaska|pollock|heik|pangaas|tilaapia|hoki|kastmes", (250, 2600))
ing("raim", "Räim", "g", "kala", 140, 18,
    ["räim", "räimefilee", "räimed", "puhastatud räimed"], [r"räim"],
    r"suitsu|soola|marin|vürts|äädik|õlis|õli\b|tomati|konserv|praetud|paneer|kotlet|pihv|frikadell|salat|"
    r"pasteet|määre|kilu|sprot|rull|hapukoores|kastmes|tilli|sinepi|sibula|keedu|krõbe|kuivatatud|kassi|koera|"
    r"karbis|kalakarp|leib|võileib|sült|tarretis|tarrendis", (200, 2600))
ing("kilu", "Vürtsikilufilee", "g", "kala", 200, 18,
    ["vürtsikilu", "vürtsikilu filee", "kilufilee"], [r"kilu"],
    r"tomati|õlis|õli\b|suitsu|sprot|pasteet|määre|võie|salat|kotlet|praetud|kassi|koera|leib|võileib|"
    r"munavõi|sinepi|tilli|hapukoore|kreem|kastmes|kaste|krõps|snäkk", (80, 1100), loose=False)
ing("heeringas", "Soolaheeringafilee", "g", "kala", 220, 17,
    ["heeringafilee", "soolaheeringas", "heeringas"], [r"heeringa|heeringas"],
    r"hapukoore|kastmes|kaste|salat|pasteet|määre|rull|marineeritud|marin|äädik|sinepi|tilli|sibula|vürtsi|"
    r"tomati|kassi|koera|suitsu|grill|praetud|leib|võileib|vorm\b|kaaviar|mari\b|veinikastmes|apelsini|koore|"
    r"jogurti|majoneesi|kurgi|peedi|porgandi|seene|seente|karri|forshmak|kreem|munaga|juurvilja|köögivilja|maitseain",
    (150, 1600), loose=False)
# Piim, kuivained, konservid, leib
ing("keefir", "Keefir", "ml", "piim", 50, 3.2,
    ["keefir", "keefir 2,5%"], [r"keefir"],
    r"maasika|vaarika|mustika|banaani|vanilli|šokolaadi|kakao|mee\b|marja|puuvilja|kirsi|kohuke|jogurt|kreem|"
    r"kook|jäätis|smuuti|laktoosivaba|kaera|soja|kookos|taim|vegan|pulber|juuretis|starter|valgu|proteiin|"
    r"\d+\s*x\s*\d|ploomi|astelpaju|rabarberi|lisandiga|kitse|kiudainete|müsli|helveste", (450, 2100),
    loose=False, ready=False)
ing("kama", "Kama", "g", "kuiv", 350, 13,
    ["kama", "kamajahu"], [r"(^|\s)kama(jahu)?\b"],
    r"kook|tort|kohuke|jäätis|jogurt|batoon|baton|küpsis|šokolaad|kommi|kompvek|tahvel|jook|kokteil|smuuti|"
    r"kreem|mousse|vaht|leib|sai\b|müsli|helbed|valgu|proteiin|kamaga|kama-|mini\b|portsjon|kotike|pirukas|"
    r"trühvel|kohupiima|keefir|gefilus|piima|muffin", (200, 1100), loose=False)
ing("pudruriis", "Ümarateraline pudruriis", "g", "kuiv", 350, 7,
    ["ümarateraline riis", "pudruriis", "riis ümarateraline"],
    [r"riis", r"ümar|pudru|camolino|lühiteraline|short\s*grain|pudrusse"],
    r"puder\b|kiir|keedukot|kotike|portsjon|helbed|jahu|piim|kook|risot|arborio|sushi|metsik|pruun|täistera|mikro|"
    r"vahvl|krõbe|kreem|desert|magustoit|pikateraline|basmati|jasmiini|parboiled|aurutatud|mahe|bio\b|organic|"
    r"\d+\s*x\s*\d+", (400, 2100), loose=False)
ing("riisinuudlid", "Riisinuudlid", "g", "kuiv", 360, 6,
    ["riisinuudlid", "rice noodles", "pad thai nuudlid"],
    [r"riisi\s*nuudl|riisinuudl|rice\s*noodle|rice\s*stick|pad\s*thai\s*nuudl|riisi\s*vermiš|vermicelli"],
    r"kiir|instant|maitsest|maitse|tassis|kauss|cup|kana|krevet|veise|köögivilja|liha|supp|karri|tšilli|chili|"
    r"valmis|komplekt|kit\b|kaste|kastmega|seesami|soja|tom yum|pho|vokin|klaas|nisu|muna|tatra|udon|ramen",
    (150, 1100), loose=False)
ing("maapahklid", "Maapähklid (röstitud)", "g", "kuiv", 585, 25,
    ["maapähklid", "röstitud maapähklid", "soolatud maapähklid"], [r"maapähkl|maa\s*pähkl"],
    r"või\b|võie|pasta|kreem|batoon|baton|šokolaad|kommi|kompvek|glasuur|mee\b|meega|mesi|karamell|kook|küpsis|"
    r"jäätis|krõps|chips|segu|pähklisegu|rosina|kassi|koera|lind|linnu|tihase|õli|jahu|valgu|proteiin|wasabi|"
    r"tšilli|chili|paprika|grill|bbq|kastmes|kaste|koores|koorega|koortega|kooreta\s*ja|dražee|jogurti|kakao|vürts|maitsest|"
    r"müsli|maapähklikr",
    (100, 1100), loose=False)
ing("punasedoad", "Punased oad (konserv)", "g", "kons", 90, 6,
    ["punased oad", "punased oad konserv", "kidney oad"], [r"oad|uba|bean", r"punase|punased|kidney"],
    r"kuivatatud|kuiv\b|tomati|tšilli|chili|kastmes|kaste|salat|segu|mehhiko|burrito|taco|valged|mustad|aed|"
    r"rohelised|kaunad|külm|külmutatud|soja|pasta|vürts|maitsest|suitsu|peekoni|lihaga|köögivilja|mahe|bio\b|"
    r"organic", (200, 450), loose=False)
ing("pohlamoos", "Pohlamoos", "g", "kons", 200, 0.3,
    ["pohlamoos", "pohlad suhkruga", "hõõrutud pohlad"], [r"pohla", r"moos|suhkru|keedis|džemm|hõõrutud|toormoos"],
    r"jogurt|kohuke|kook|küpsis|pirukas|sai\b|vahvel|tort|kreem|jäätis|kompvek|šokolaadi|kommi|mahl|jook|siirup|"
    r"smuuti|kissell|tee\b|leib|portsjon|kotike|vesi|vein|liköör|suhkruvaba|kohupiima|juustu|kaste|kastmes|"
    r"õuna|maasika|jõhvika|mustika|vaarika|pirni", (200, 1100), loose=False)
ing("kalakaste", "Kalakaste", "ml", "kons", 35, 5,
    ["kalakaste", "fish sauce"], [r"kala\s*kaste|kalakaste|fish\s*sauce"],
    r"ostri|oyster|sojakaste|sriracha|tšilli|chili|magus|krõps|nuudl|vürts|maitseaine|segu|kassi|koera|vegan",
    (60, 1100), loose=False, ready=False)
ing("tahini", "Tahini (seesamipasta)", "g", "kons", 600, 17,
    ["tahini", "seesamipasta"], [r"tahin|seesamipasta|seesami\s*pasta"],
    r"kaste|kastmes|halvaa|halva|hummus|batoon|kommi|šokolaad|küpsis|leib|sai\b|segu|maitsest|krõps|snäkk|"
    r"mini\b|portsjon|kakao", (150, 1100), loose=False, ready=False)
ing("oliivioli", "Oliiviõli", "ml", "kons", 820, 0,
    ["oliiviõli", "ekstra neitsioliiviõli", "oliiviõli extra virgin"], [r"oliiviõli|olive\s*oil|oliivi\s*õli"],
    r"sprei|spray|maitsest|küüslaugu|ürdi|tšilli|chili|basiiliku|sidruni|trühvli|majonees|margariin|kala|kilu|"
    r"sprot|tuunikala|õlis|õliga|oliivid|seep|kosmeet|keha|juuksi|naha|massaaž|lamp|pomace|jäägi|segu|rapsi|"
    r"päevalille|kook|leib|sai\b|krõps|snäkk|pesto|kaste|mini\b|\d+\s*x\s*\d|šampoon|shampoo|kreeker", (250, 3100),
    loose=False,
    pantry=True, ready=False)
ing("sai", "Sai (valge leib)", "g", "leib", 260, 8,
    ["sai", "röstsai", "viilutatud sai", "valge sai"], [r"(^|\s)(rost)?sai\b|röstsai|saiapäts|nisusai"],
    r"saiake|kukkel|kuklid|sarvesai|croissant|kaneeli|kringel|rosina|kohupiima|moosi|vanilli|šokolaadi|kreemi|"
    r"juustu|küüslaugu|seemne|seemnetega|rukki|leib|täistera|gluteenivaba|hot ?dog|burger|riivsai|krutoon|"
    r"kreeker|näkk|keeks|kook|tort|pirukas|pitsa|pizza|vorst|viiner|sink|kana|mini\b|külmutatud|toorik|tainas|"
    r"taigen|kõrvitsa|kaera|spelta|maisi|kartuli|mee\b|kakao|kommi|müsli|valgu|proteiin|kama|piima|magus|"
    r"vahvli|pannkoogi|muffin|toast|kiud|rosinatega|pähkli|kartulisai", (200, 1100), loose=False)

ing("sinimerekarbid", "Sinimerekarbid (kodades)", "g", "kala", 26, 3.6,
    ["sinimerekarbid", "sinimerekarbid kodades", "rannakarbid"], [r"sinimerekarb|sinimerekarp|rannakarb|mussel"],
    r"kastmes|kaste|marin|soolvees|õlis|konserv|salat|pasteet|vürts|küüslaugu|tomati|veini|koore|juustu|paneer|"
    r"kooritud|liha\b|lihad|segu|mereandide|kassi|koera|valmis|kuumsuits|suitsu|pooles\s*kojas|poolkodades",
    (400, 3100))
ing("vein", "Kuiv valge vein", "ml", "kons", 82, 0.1,
    ["kuiv valge vein", "valge vein kuiv", "valge vein"],
    [r"(vein|wine|vino|vin\b).*(valge|white|blanc|bianco)|(valge|white|blanc|bianco).*(vein|wine|vino)|chardonnay|"
     r"sauvignon|chenin|riesling|grigio|soave|furmint|verdejo|albari|grüner|semillon|muscadet|vinho verde|gavi\b|"
     r"macabeo|airen|(^|\s)blanc\b"],
    r"poolmagus|magus|poolkuiv|vahuvein|šampan|champagne|prosecco|cava|crémant|alkoholivaba|alk\.?\s*vaba|"
    r"0[,.]0\s*%|bag|kott|kast\b|\d+\s*x\s*\d|glögg|punane|roosa|rosé|äädikas|kaste|kook|kokteil|siider|"
    r"sangria|spritz|maitsestatud|aromatiseeritud|portvein|šerri|vermut|marsala|puuvilja|marja|õuna|"
    r"kingituse|karbis|komplekt|klaasid|klaas\b|kastmes|vähid|krevet|moscato|muskat|kabinett|spätlese|auslese|"
    r"lieblich|halbtrocken|semi|dulce|amabile|dolce|medium|sweet|brut|frizzante|spumante|sekt\b|demi|ice\s*wine|jäävein|"
    r"punane|red\b|rosso|tinto|merlot|cabernet|shiraz|syrah|malbec|tempranillo|primitivo|zinfandel|noir\b",
    (187, 1000), loose=False, ready=False)

ing("pardikoivad", "Pardikoivad", "g", "liha", 180, 17,
    ["pardikoivad", "pardi koivad", "pardikoib", "pardi reied"], [r"pardi|part\b", r"koib|koiva|reie|kints"],
    r"konfit|confit|marin|suitsu|grill|valmis|praetud|küpsetatud|hautatud|sous|vide|maitsest|kassi|koera|rinna|"
    r"filee|kana|broiler|kalkun|hane|pasteet|rillette|kotlet|pärane|kauak|premium", (300, 3100))
# ---------------------------------------------------------------- Kiired road (Mihkel 7.11.2026: "inimestel on pidevalt kiire")
ing("ubatomatis", "Oad tomatikastmes (konserv)", "g", "kons", 80, 4.7,
    ["oad tomatikastmes", "valged oad tomatikastmes", "baked beans"],
    [r"oad|uba|ube|beans|beanz|bean", r"tomati|baked"],
    r"chili|tšilli|vürts|lihaga|peekoni|vorsti|mehhiko|salat|kuivatatud|punased|kidney|mustad|rohelised|herne|"
    r"kikerhern|läätse|suitsu|maitsest|karri|külm|organic|mahe", (200, 1100), loose=False, ready=False)
ing("gnocchi", "Gnocchi (kartulist)", "g", "kulm", 150, 3.5,
    ["gnocchi", "kartuli gnocchi", "njokid"], [r"gnocchi|njok"],
    r"kaste|kastmes|valmis|juustu|spinati|bataadi|kõrvitsa|täidis|täidetud|pesto|tomati|seene|vegan|"
    r"gluteenivaba|portsjon|pasta|muna|köögivilj|ahjus|truffle|trühvli|makaron", (300, 1100), loose=False, ready=False)
ing("kuskuss", "Kuskuss", "g", "kuiv", 360, 13,
    ["kuskuss", "couscous"], [r"kuskuss|couscous|kus-kuss"],
    r"salat|valmis|maitsest|köögivilja|portsjon|kiir|kana|tomati|ürdi|kauss|mahe|bio\b|organic|täistera|"
    r"pärl|israeli|segu", (250, 1100), loose=False)
ing("pesto", "Basiilikupesto", "g", "kons", 450, 5,
    ["pesto", "basiilikupesto", "pesto genovese"], [r"pesto"],
    r"punane|rosso|tomati|päikesekuivatatud|vegan|küüslaugu|kõrvitsa|karulaugu|spinati|krõps|leib|sai\b|"
    r"pasta\b|pitsa|pizza|kana|juust|kreeker|ravioli|tortell|gnocchi|salat|pähkli|rukola|lehtkapsa|kale|"
    r"avokaado|herne|peedi|tšilli|chili|mini\b|määre|võileiva|karul", (90, 600), loose=False, ready=False)
ing("feta", "Fetajuust", "g", "piim", 260, 15,
    ["feta", "fetajuust", "salatijuust", "feta juust"], [r"feta|salatijuust|fetaki"],
    r"määre|maitsest|ürdi|õlis|marineeritud|pirukas|salat\b|kreem|küüslaugu|tšilli|chili|oliivi|tomati|"
    r"spinati|paprika|vegan|taim|krõps|pasta|lehttaigna|kuubikud\s*õlis|mee\b|pähkli|kitse|lamba|ürti|laktoosivaba",
    (100, 1100),
    loose=False)

# ---------------------------------------------------------------- Puuduvad road (Mihkel 8.11.2026: "lisa need retseptid mis on puudu")
ing("lillkapsas", "Lillkapsas", "g", "puu", 25, 1.9,
    ["lillkapsas"], [r"lillkapsas"],
    r"külm|külmutatud|riis|püree|pitsa|brokoli|segu|gratään|vorm\b|praetud|röstitud|salat|supp|kotlet|pasta|"
    r"mini\b|beebi|romanesco|lilla|oranž|kollane|roheline|mahe|bio\b|organic|marineeritud|hapendatud|tükeldatud|"
    r"juustu|kastmes|krõps|snäkk", (300, 2100), piece=600)
ing("korvits", "Kõrvits", "g", "puu", 40, 1.0,
    ["kõrvits", "muskaatkõrvits", "hokkaido kõrvits", "butternut kõrvits"], [r"kõrvits|butternut"],
    r"suvikõrvits|seemne|seemned|õli|püree|supp|pirukas|külm|külmutatud|kuubik|tükid|krõps|marineeritud|"
    r"hoidis|moos|leib|sai\b|pasta|ravioli|tortell|gnocchi|kook|muffin|kreem|dekoratiiv|kaunistus|mini\b|"
    r"mahe|bio\b|organic|kõrvitsaga|pesto|mahl|jook|salat|risotto|riivitud|viilud|ahju|grill",
    (500, 4100), piece=1000)
ing("ricotta", "Ricotta", "g", "piim", 150, 9,
    ["ricotta", "ricotta juust"], [r"ricotta"],
    r"pasta|ravioli|tortell|cannelloni|lasanje|kook|spinati|pirukas|mascarpone|salat|valmis|vegan|taim|kreem",
    (200, 1100), loose=False)
ing("lehttainas", "Lehttainas", "g", "kulm", 400, 6,
    ["lehttainas", "pärmilehttainas", "lehttainas külmutatud"], [r"lehttai|lehttaign"],
    r"pirukas|pirukad|saiake|saiakesed|sarvik|\brull\b|kook|kringel|täidis|täidetud|vorst|juustu|singi|moosi|"
    r"õuna|kohupiima|pitsa|vahvl|küpsis|pulgad|snäkk|kaneeli|vanilli|šokolaadi|kreemi|ruudud|kotlet|pähkli|"
    r"mooni|seemne|krõps", (200, 1600), loose=False)
ing("kanamaks", "Kanamaks", "g", "liha", 120, 17,
    ["broileri maks", "kanamaks", "broileri maksad", "kana maks"], [r"maks", r"broiler|kana|br\."],
    r"pasteet|pate\b|paté|määre|vorst|pirukas|pelmeen|kaste|seamaks|sea\s|veise|maksarull|praetud|konserv|"
    r"koera|kassi|lemmik|süda|südamed|magu|maod|kõht|kaela|tiiva|marin|maitsest|kalkun|pardi|hane|kala|moorits",
    (300, 2100))
ing("searibid", "Searibid", "g", "liha", 220, 13,
    ["searibid", "sea ribid", "searibi", "sea ribi", "searibikesed"], [r"ribi", r"sea"],
    r"suitsu|suits\.|marin|maitsest|grill|bbq|küpsetatud|praetud|valmis|sous|vide|keedu|keedetud|kalkun|veise|"
    r"kana|broiler|lamba|krõps|mee\b|mesi|sinepi|küüslaugu|vürts|koore|kastmes|kaste|glasuur|teriyaki|tšilli|"
    r"chili|paprika|ahju|hautatud|supi|õlle|õllega|korea|hiina|ameerika|texas", (500, 3100))
ing("seakoot", "Seakoot või seajalad (süldiks)", "g", "liha", 150, 14,
    ["seakoot", "sea koot", "seajalad", "sea jalad", "sea kintsukoot"], [r"sea", r"koot|jal"],
    r"suitsu|suits\.|keedu|keedetud|grill|marin|ahju|küpsetatud|kana|broiler|veise|lamba|kalkun|sült|valmis|"
    r"vorst|hautatud|eisbein|konserv|koera|kassi|lemmik|krõps|närimis|maitsest|õlle", (500, 4100))
ing("ananass", "Ananass (konserv)", "g", "kons", 60, 0.4,
    ["ananassitükid", "ananass konserv", "ananassiviilud", "ananassitükid mahlas"], [r"ananass"],
    r"mahl\b|jook|nektar|kuivatatud|kook|jogurt|moos|komm|smuuti|siirup\b|värske|külmutatud|puuviljasegu|"
    r"kokteil|segu|tee\b|krõps|chips|mango|papaia|kookos|kohupiima|pirukas|kreem|tarretis|želee|vesi\b|"
    r"kompvek|komm|alkohol|long\s*drink|maitseline|maitsega|karastus|juust|külm|šokolaad|jäätis",
    (150, 900), loose=False, drained=True)

# ---------------------------------------------------------------- Asendused (Mihkel 8.11.2026: allergiad)
# Gluteeni- ja piimavabad asendused: kui keegi lauas neid ei söö, tehakse roog asendusega (Catalog.swaps).
GV = r"gluteenivaba|gluteeni\s*vaba|gluten\s*free|glutenfree|gluteenita"
ing("gvpasta", "Gluteenivaba pasta", "g", "kuiv", 355, 7,
    ["gluteenivaba pasta", "gluteenivabad spagetid", "gluteenivaba makaron", "gluteenivaba fusilli"],
    [GV, r"pasta|spaget|makaron|fusilli|penne|farfalle|tagliatelle|fettuccine|rigatoni|tortiglioni"],
    r"valmis|kaste|lasanje|nuudl|riisinuudl|kinoa|lääts|kikerhern|herne|\boa\b|ubade|soja|edamame|"
    r"lapse|beebi|mini\b|täidis|ravioli|tortell|gnocchi", (200, 1100), loose=False, ready=False)
ing("gvleib", "Gluteenivaba leib või sai", "g", "leib", 250, 3,
    ["gluteenivaba leib", "gluteenivaba sai", "gluteenivaba röstsai", "gluteenivaba seemneleib"],
    [GV, r"leib|sai\b|saiake|röstsai|seemneleib|vormileib|ciabatta|bread|brot"],
    r"kook|küpsis|jahu|segu|riivsai|näkileib|krõbe|pitsa|burger|hot\s*dog|vahvl|kreeker|krõps|muffin|"
    r"šokolaad|kaneeli|moosi|biskviit|külmutatud|valmistamiseks", (180, 900), loose=False, ready=False)
ing("gvjahu", "Gluteenivaba jahusegu", "g", "kuiv", 355, 4,
    ["gluteenivaba jahu", "gluteenivaba jahusegu", "gluteenivaba küpsetussegu", "gluteenivaba universaalne jahu"],
    [GV, r"jahu|segu|mix"],
    r"leiva|pannkoogi|koogi|muffin|pitsa|vahvl|küpsise|šokolaadi|kreekeri|pasta|brownie|biskviidi|"
    r"tatra|riisi|maisi|kaera|mandli|kookose|kikerherne|kartuli|tärklis", (400, 1100), loose=False, ready=False)
ing("gvkaer", "Gluteenivabad kaerahelbed", "g", "kuiv", 370, 13,
    ["gluteenivabad kaerahelbed", "gluteenivaba kaerahelbed", "gluteenivabad kiirkaerahelbed", "elovena gluteenivaba"],
    [GV, r"kaerahelb|kaera\s*helb|kiirkaerahelb|kaerahelv"],
    r"puder\b|pudru|küpsis|batoon|müsli|granola|jook|jahu|kliid|maitse|mari|marja|šokolaad|instant|"
    r"portsjon|karbis|topsis|näkileib|vahepala", (300, 1100), loose=False, ready=False)
ing("tamari", "Tamari (gluteenivaba sojakaste)", "ml", "kons", 70, 10,
    ["tamari", "tamari sojakaste", "gluteenivaba sojakaste"],
    [r"tamari|gluteenivaba\s*soja|soja\w*\s*gluteenivaba"],
    r"marinaad|teriyaki|wok|magus|sweet|küüslaugu|tšilli|chili|seesami|ingveri|vähendatud", (100, 1100),
    loose=False, ready=False)
# ainult gluteenivabaks märgitud: tavalistes maisitortillades on sageli ka nisujahu
ing("gvtortillad", "Gluteenivabad tortillad", "g", "leib", 230, 4,
    ["gluteenivabad tortillad", "gluteenivaba tortilla", "tortilla gluteenivaba", "gluteenivaba wrap"],
    [GV, r"tortill|tortij|wrap"],
    r"krõps|chips|nacho|kit\b|komplekt|taco\s*kest|kestad|shell|kaste|salsa", (150, 900), loose=False, ready=False)
# kaerajook ainult gluteenivaba märgisega: sobib ka siis, kui keegi ei söö gluteeni ega piimatooteid
ing("kaerajook", "Kaerajook (gluteenivaba)", "ml", "piim", 45, 1,
    ["gluteenivaba kaerajook", "kaerajook gluteenivaba", "kaerajook laktoosi- ja gluteenivaba", "kaerajook"],
    [r"kaera", r"jook|drink", GV],
    r"šokolaadi|kakao|kohvi|maasika|vanilli|banaani|jogurt|smuuti|kook|helbe|küpsis|jäätis|kohvikoor|"
    r"mini\b|lastele|baby|proteiin|valgu|pistaatsia|maitseline|maitsega", (900, 2100), loose=False, ready=False)
# ainult piimavabaks märgitud määre (tavaline margariin võib sisaldada pett- või piimapulbrit)
ing("taimvoi", "Vegan määre", "g", "piim", 520, 0.2,
    ["vegan määre", "vegan võie", "taimne võie", "naturale vegan"],
    [r"vegan|piimavaba|maidoton|dairy\s*free|naturale", r"määre|võie|või\b|butter"],
    r"juust|toorjuust|küüslaugu|ürdi|šokolaadi|pähkli|kook|leib|võileivamääre|kreem|kala|sink|liha",
    (150, 600), loose=False, ready=False)
ing("kaerakoor", "Kaera köögikreem", "ml", "piim", 150, 1,
    ["kaera köögikreem", "köögikreem", "taimne köögikreem", "imat"],
    [r"kaera|soja|taimne|vegan|\bimat\b", r"köögikreem|toiduvalmistamis|cuisine|\bimat\b"],
    r"kooritud|mahl|jäätis|vahu|kohvi|šokolaad|vanilli|fraiche|fraîche|hapukoor|kookos", (200, 1100),
    loose=False, ready=False)
ing("taimjogurt", "Taimne jogurt (naturaalne)", "g", "piim", 50, 4,
    ["taimne jogurt", "sojajogurt", "alpro naturaalne", "sojavahepala naturaalne"],
    [r"soja|kaera|taim|vegan|alpro|oatly|oddlygood", r"jogurt|yogurt|yoghurt|jogurtitoode|vahepala|naturaalne"],
    r"maasika|vaarika|mustika|vanilli|šokolaadi|virsiku|mango|kirsi|puuvilja|marja|joogi|jook\b|smuuti|"
    r"lastele|kookos|kreeka|plant\s*protein", (300, 1100), loose=False, ready=False)
ing("taimjuust", "Taimne juust (Violife vms)", "g", "piim", 280, 0.5,
    ["violife", "vegan juust", "vegantoode gouda", "taimne juust"],
    [r"violife|gourmet\s*green|vegan|taimne", r"juust|viil|toode|gouda|cheddar|riiv|plokk"],
    r"toorjuust|määre|küüslaugu|ürtidega|kookosõl|valm\.?\s*toit|kreeka|pitsa|kaste|sojatoode|plant\s*protein",
    (90, 600), loose=False, ready=False)
ing("taimfraiche", "Kaerakreem (hapukoore asemel)", "g", "piim", 160, 1,
    ["kaerakreem", "fermenteeritud kaerakreem", "kaerakreem originaal", "kaerafraiche"],
    [r"kaera|taim|vegan|oat|soja", r"kreem|fraiche|fraîche"],
    r"köögikreem|jook|pistaatsia|maitseline|maasika|vaarika|šokolaadi|vanilli|kohvi|krõps|näkileib",
    (150, 600), loose=False, ready=False)

ING = {x["id"]: x for x in I}
assert len(ING) == 149, len(ING)
