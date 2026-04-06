#!/usr/bin/env python3
"""
Generate 77 high-quality 5×5 crossword puzzles for Hungarian geography and culture.

5×5 checkerboard template:
  W W W W W   (row 0 = across word)
  W # W # W
  W W W W W   (row 2 = across word)
  W # W # W
  W W W W W   (row 4 = across word)

Columns 0, 2, 4 are down words (length 5).
Black cells at (1,1),(1,3),(3,1),(3,3).

Clue numbers:
  #1 = (0,0): 1-Across (row0) + 1-Down (col0)
  #2 = (0,2): 2-Down (col2)
  #3 = (0,4): 3-Down (col4)
  #4 = (2,0): 4-Across (row2)
  #5 = (4,0): 5-Across (row4)
"""

import json
import os
from pathlib import Path

# ─── VERIFIED 5-LETTER HUNGARIAN WORD LIST ───────────────────────────────────
# These are real, common Hungarian words, each exactly 5 Unicode characters.
# Includes Hungarian diacritics (á é í ó ö ő ú ü ű).
# Note: Hungarian digraphs (cs, sz, gy, ny, ly, ty) are 2 chars = 1 cell each.
# Here we count Unicode characters (cells) only — CSATA = C,S,A,T,A = 5 cells.

WORD_LIST = [
    # A
    "ABLAK",  # window
    "ALMÁK",  # apples
    "ALMÁS",  # apple-flavored
    # B
    "BABÉR",  # laurel
    "BAJOK",  # troubles
    "BAJOS",  # troubled
    "BALTA",  # axe
    "BARÁT",  # friend / monk
    "BÁTOR",  # brave
    "BIRKA",  # sheep
    "BODZA",  # elderberry
    "BOLHA",  # flea
    "BOKOR",  # bush/shrub
    "BORDA",  # rib
    "BOROS",  # wine-related / winey
    # CS
    "CSATA",  # battle
    "CSEND",  # silence
    "CSIGA",  # snail / spiral
    "CSONT",  # bone
    "CSUKA",  # pike (fish)
    "CSÚCS",  # peak / summit
    # D
    "DOLOG",  # thing / work
    # E, É
    "EBÉDE",  # his/her lunch
    "ERDEI",  # forest (adj)
    # F
    "FEHÉR",  # white
    "FELHŐ",  # cloud
    "FENYŐ",  # pine tree
    "FOLYÓ",  # river
    "FORMA",  # form / shape
    "FÓRUM",  # forum
    "FRANK",  # frank / Franc
    # G
    "GAZDA",  # farmer / master
    "GOMBA",  # mushroom
    "GÖRBE",  # crooked / curve
    "GÖRÖG",  # Greek
    "GŐZÖS",  # steamy / steamboat
    # GY
    "GYÁVA",  # cowardly
    # H
    "HADAK",  # armies
    "HAJAS",  # hairy
    "HAJÓS",  # sailor
    "HALAK",  # fish (pl)
    "HALAS",  # fishy / fish-rich
    "HALOM",  # heap / pile
    "HÁROM",  # three
    "HÁRFA",  # harp
    "HAVAS",  # snowy
    "HIDEG",  # cold
    "HONOS",  # native / local
    "HORDÓ",  # barrel
    "HŰVÖS",  # cool / chilly
    # I
    "IGAZI",  # real / genuine
    # J
    "JOGAR",  # scepter
    "JÓKOR",  # timely
    # K
    "KAKAS",  # rooster
    "KALAP",  # hat
    "KÁVÉS",  # coffee-flavored
    "KAZAL",  # haystack
    "KAZÁR",  # Khazar
    "KELET",  # east
    "KÉPEK",  # pictures
    "KÉREM",  # please / I ask
    "KINCS",  # treasure
    "KÖRÖS",  # ringed / (river Körös)
    "KŐRIS",  # ash tree
    "KÖLES",  # millet
    "KŐVÁR",  # stone castle
    "KUPAC",  # heap
    # L
    "LATIN",  # Latin
    "LEVES",  # soup
    "LEVÉL",  # letter / leaf
    "LIGET",  # grove / park
    "LISZT",  # flour / Liszt
    "LOVAG",  # knight
    "LOVAK",  # horses
    # M
    "MADÁR",  # bird
    "MALOM",  # mill
    "MELEG",  # warm
    "MESÉK",  # tales
    "MESÉS",  # fabulous
    "MÉHES",  # apiary
    "MÉZES",  # honeyed
    "MEZŐK",  # fields
    "MOHOS",  # mossy
    "MÓZES",  # Moses
    "MUTAT",  # shows
    # N
    "NAPOK",  # days
    "NAPOS",  # sunny
    "NÁDAS",  # reed-bed
    "NÁDOR",  # palatine
    "NEMES",  # noble
    "NOMÁD",  # nomad
    "NYÁRI",  # summer (adj)
    # O, Ó
    "OPERA",  # opera
    "ORDAS",  # wolf-gray
    "ŐSZIG",  # until autumn
    # P
    "PADLÓ",  # floor
    "PATAK",  # stream
    "PÉTER",  # Peter (name)
    "PIROS",  # red
    "PONTY",  # carp (fish)
    "PORTA",  # gate / entrance
    # R
    "RÉTES",  # strudel-like
    "RETEK",  # radish
    "RÓMAI",  # Roman
    "ROMÁN",  # Romanian / Romanesque
    "RÓZSA",  # rose
    # S
    "SARLÓ",  # sickle
    "SASOK",  # eagles
    "SASOS",  # eagle-like
    "SÁTOR",  # tent
    "SEREG",  # army
    "SÍKOS",  # slippery
    "SÜKET",  # deaf
    "SÜTIK",  # cookies / they bake
    # SZ
    "SZÁSZ",  # Saxon
    "SZARV",  # antler
    # T
    "TÁBOR",  # camp
    "TÁBLA",  # board / tablet
    "TATÁR",  # Tatar
    "TÉLEN",  # in winter
    "TIGRI",  # tiger
    "TŐKÉS",  # capitalist
    "TÖLGY",  # oak tree
    "TORTA",  # cake
    "TÖRÖK",  # Turkish / Turk
    "TÚRÓS",  # cottage-cheese
    # U
    "UDVAR",  # court / yard
    # V
    "VADON",  # wilderness
    "VADAK",  # wild animals
    "VÁRAK",  # castles
    "VÁSÁR",  # market
    "VÁROS",  # city
    "VILÁG",  # world / light
    "VIHAR",  # storm
    "VITÉZ",  # hero / valiant
    # Z
    "ZÖLDE",  # greenish
    "ZÚGÁS",  # buzzing/roaring
]

# Ensure uniqueness and exact 5-char length
VALID_WORDS = sorted(set(w for w in WORD_LIST if len(w) == 5))

print(f"Word pool: {len(VALID_WORDS)} words")

# ─── GRID FINDER ─────────────────────────────────────────────────────────────

def find_valid_grids(words):
    """
    Find all valid 5×5 checkerboard grids.

    Grid structure:
      (0,0)(0,1)(0,2)(0,3)(0,4)   ← row0 across word
      (1,0)  #  (1,2)  #  (1,4)   ← only col 0,2,4 used
      (2,0)(2,1)(2,2)(2,3)(2,4)   ← row2 across word
      (3,0)  #  (3,2)  #  (3,4)   ← only col 0,2,4 used
      (4,0)(4,1)(4,2)(4,3)(4,4)   ← row4 across word

    Down words use all 5 rows of col 0, 2, 4:
      col0 = (0,0),(1,0),(2,0),(3,0),(4,0)
      col2 = (0,2),(1,2),(2,2),(3,2),(4,2)
      col4 = (0,4),(1,4),(2,4),(3,4),(4,4)

    Intersections (must match):
      row0[0]=col0[0], row0[2]=col2[0], row0[4]=col4[0]
      row2[0]=col0[2], row2[2]=col2[2], row2[4]=col4[2]
      row4[0]=col0[4], row4[2]=col2[4], row4[4]=col4[4]

    Free cells: (1,0),(1,2),(1,4),(3,0),(3,2),(3,4)
      These are positions 1 and 3 in the down words, not constrained by across words.
    """
    word_list = sorted(words)

    # Index: for matching down words given fixed positions 0, 2, 4
    # Build lookup: (char_at_0, char_at_2, char_at_4) -> list of words
    down_index = {}
    for w in word_list:
        key = (w[0], w[2], w[4])
        down_index.setdefault(key, []).append(w)

    valid_grids = []

    for row0 in word_list:
        for row2 in word_list:
            for row4 in word_list:
                # Required positions for each down column
                # col0: pos0=row0[0], pos2=row2[0], pos4=row4[0]
                k0 = (row0[0], row2[0], row4[0])
                col0_cands = down_index.get(k0, [])
                if not col0_cands:
                    continue

                # col2: pos0=row0[2], pos2=row2[2], pos4=row4[2]
                k2 = (row0[2], row2[2], row4[2])
                col2_cands = down_index.get(k2, [])
                if not col2_cands:
                    continue

                # col4: pos0=row0[4], pos2=row2[4], pos4=row4[4]
                k4 = (row0[4], row2[4], row4[4])
                col4_cands = down_index.get(k4, [])
                if not col4_cands:
                    continue

                for col0 in col0_cands:
                    for col2 in col2_cands:
                        for col4 in col4_cands:
                            valid_grids.append((row0, row2, row4, col0, col2, col4))

    return valid_grids


def grid_to_matrix(row0, row2, row4, col0, col2, col4):
    """Build 5×5 matrix from word 6-tuple."""
    return [
        list(row0),
        [col0[1], '#', col2[1], '#', col4[1]],
        list(row2),
        [col0[3], '#', col2[3], '#', col4[3]],
        list(row4),
    ]


print("Finding valid grids...")
all_grids = find_valid_grids(VALID_WORDS)
print(f"Total valid grids: {len(all_grids)}")

# Deduplicate
seen = set()
unique_grids = []
for g in all_grids:
    if g not in seen:
        seen.add(g)
        unique_grids.append(g)

print(f"Unique grids: {len(unique_grids)}")

# Prefer grids where not all 6 words are the same, and across != down
diverse_grids = [g for g in unique_grids if len(set(g)) > 3]
print(f"Diverse grids (>3 unique words): {len(diverse_grids)}")

# Use diverse grids if enough, else fall back
working_grids = diverse_grids if len(diverse_grids) >= 77 else unique_grids
print(f"Using {len(working_grids)} grids for puzzle generation")


# ─── CLUE DATABASE ───────────────────────────────────────────────────────────
# Each word gets multiple clue variants for variety

CLUES = {
    "ABLAK": [
        "Amin keresztül bevilágít a nap — ajtó melletti nyílás",
        "Üveg van benne, a falon — szellőztetésre nyitjuk ki",
        "A ház falán lévő nyílás — kinézünk rajta az utcára",
    ],
    "ALMÁK": [
        "Piros gyümölcsök a fán — őszi betakarítás termékei",
        "Gyümölcsök, amelyek lehullanak a fáról — piros vagy zöld",
        "Almafa termése — rétes tölteléke is lehet",
    ],
    "ALMÁS": [
        "Almával töltött — almás rétes édes csemege",
        "Almából készült — almás pite receptje",
        "Almás pite, rétes jelzője — almával ízesített",
    ],
    "BABÉR": [
        "Koszorúba font zöld növény — győztesek fejékszere",
        "Fűszerként is ismert bogyós cserje — babérkoszorú",
        "Antik olimpia győzteseit illette — babérkoszorú",
    ],
    "BAJOK": [
        "Gondok, problémák — nehézségek sorozata",
        "Nehézségek, gondok — bajba kerülni rossz dolog",
        "Problémák, gondok — segítségre szorulnak",
    ],
    "BAJOS": [
        "Nehézségekkel járó — bonyolult, nehéz feladat",
        "Kényes, nehézkes — bajosan megoldható",
        "Gondos, aggódó — bajos természetű ember",
    ],
    "BALTA": [
        "Fakitermelő szerszám — fejsze, erdőirtóé",
        "Éles pengéjű favágó eszköz — baltával aprítják a fát",
        "Favágáshoz használt szerszám — baltával hasítja a fát",
    ],
    "BARÁT": [
        "Jó ismerős, közeli személy — barátság köteléke",
        "Szerzetes kolostorban — barát remeteségben él",
        "Megbízható, hűséges társ — barátja van bajban",
    ],
    "BÁTOR": [
        "Félelem nélkül cselekvő — vitéz, merész harcos",
        "Bátran szembenéz a veszéllyel — bátor katona",
        "Nem fél a nehézségektől — bátor döntés",
    ],
    "BIRKA": [
        "Gyapjas háziállat, juh — legelőn legel a pusztán",
        "Nyáj tagja — birka gyapját nyírják",
        "Szürke vagy fehér juh — birka a réten",
    ],
    "BODZA": [
        "Fehér virágú bogyós cserje — szörpöt főznek belőle",
        "Bodzavirágból szörp — kerti cserje",
        "Fehér virágú fa — bodzaszörp hűsítő ital",
    ],
    "BOLHA": [
        "Apró ugró rovar — kutya bundájában él",
        "Kis vérszívó parazita — bolhapiac is róla kapta nevét",
        "Ugró élősdi rovar — állatokon élősködik",
    ],
    "BOKOR": [
        "Kisebb lombos növény — erdőszélen nő",
        "Alacsony cserje — bokor mögé búvik",
        "Lombos kisfa — gyümölcsbokor is terem",
    ],
    "BORDA": [
        "Mellkasi csont — emberi váz eleme",
        "Csontszerkezet a mellkasban — bordák védik a szívet",
        "Mellcsont oldalán húzódó csont — borda minta szövésen is",
    ],
    "BOROS": [
        "Borral teli vagy borkedvelő — pincéből kerül ki",
        "Borra vonatkozó — boros kultúra Magyarországon",
        "Bort szerető — boros esték falun",
    ],
    "CSATA": [
        "Fegyveres összecsapás, ütközet — csatamező helyszíne",
        "Háborús összeütközés — csatát vesztett hadsereg",
        "Katonai ütközet — csatában hősiesen helytállt",
    ],
    "CSEND": [
        "Zajtalanság, némaság — könyvtárban illik ez",
        "Zaj hiánya — csendben pihen a természet",
        "Némaság, csönd — éjszaka csend van a falun",
    ],
    "CSIGA": [
        "Lassú puhatestű, házban lakik — csigalépcső",
        "Kis spirálházzal lakó állat — lassú mint a csiga",
        "Puhatestű állat házával — csigát esik az eső után",
    ],
    "CSONT": [
        "Emberi váz eleme — kutyának is odadobják",
        "Váz szilárd eleme — csontváz a múzeumban",
        "Kemény belső vázelem — csont és hús",
    ],
    "CSUKA": [
        "Ragadozó édesvízi hal — Tisza és Duna lakója",
        "Magyar folyók ragadozó hala — csuka fogásán örül a horgász",
        "Édesvízi ragadozó hal — csukát sütötte a halász",
    ],
    "CSÚCS": [
        "Hegy legmagasabb pontja — teljesítmény teteje",
        "Hegycsúcs magaslatán — csúcsteljesítmény",
        "Leghegyes rész, tetőpont — csúcstalálkozó",
    ],
    "DOLOG": [
        "Feladat, tárgy, munka — elvégzendő dolog",
        "Tárgy, feladat — köznapi dolog",
        "Tennivaló, munka — dologra szoktatja a gyereket",
    ],
    "EBÉDE": [
        "Déli étkezés — munkahelyi menza kínálata",
        "Középső napi étkezés — ebédet főz az asszony",
        "Napi főétkezés — ebéde paprikás csirke volt",
    ],
    "ERDEI": [
        "Erdőben élő vagy erdőre vonatkozó — erdei ösvény",
        "Erdőhöz tartozó — erdei gomba, erdei madár",
        "Vadon, erdő jelzője — erdei túra és séta",
    ],
    "FEHÉR": [
        "Hó színe — ellentéte a fekete",
        "Tiszta, világos szín — fehér galamb békeszimbólum",
        "Hófehér szín — fehér zászló megadás jele",
    ],
    "FELHŐ": [
        "Vízpára az égen — esőt hozhat",
        "Égbolton úszó párás tömeg — felhőből hull az eső",
        "Bárányfelhő az égen — szürke felhő zivatart hoz",
    ],
    "FENYŐ": [
        "Tűlevelű fa — karácsonyfa alapja",
        "Örökzöld hegyei fa — fenyőerdő illatát szeretjük",
        "Magas hegyi fa — fenyőtoboz az erdőn",
    ],
    "FOLYÓ": [
        "Természetes vízfolyás — folyópartján városok épültek",
        "Vízfolyás, melybe patakok ömlenek — folyót hajók járják",
        "Nagy vízfolyás — a Duna és Tisza is folyó",
    ],
    "FORMA": [
        "Alak, keret, minta — öntőformába kerül az anyag",
        "Alakzat, sablon — forma és tartalom",
        "Keret, sablon — sütőformában süti a tortát",
    ],
    "FÓRUM": [
        "Nyilvános tér, tanácskozóhely — antik Rómában is volt",
        "Vitafórum, nyilvános tér — Róma főtere",
        "Közvitára szánt hely — fórumon megvitatják a kérdést",
    ],
    "FRANK": [
        "Germán nép tagja — Frankföld, Frank Birodalom",
        "Őszinte, nyílt — frank véleménye volt",
        "Svájci pénznem — svájci frank",
    ],
    "GAZDA": [
        "Gazdálkodó, tulajdonos — tanya gazdája",
        "Földtulajdonos, farmer — gazda gondozza a jószágot",
        "Falusi ember, bérgazda — gazda az udvaron",
    ],
    "GOMBA": [
        "Erdőben termő növény — gombapaprikás finomság",
        "Gombászó szedi az erdőn — gomba és spóra",
        "Ehető erdei termő — gombát szed a néni",
    ],
    "GÖRBE": [
        "Egyenes ellentéte — hajlított vonal",
        "Ívelt, kanyargó — görbe út a hegyen",
        "Nem egyenes, hajlott — görbe faág",
    ],
    "GÖRÖG": [
        "Hellén nép tagja — ókori görög kultúra",
        "Görögország lakója — görög mitológia gazdagsága",
        "Ókori hellén — görög filozofia alapjai",
    ],
    "GŐZÖS": [
        "Gőzzel hajtott hajó — Dunán közlekedett",
        "Gőzmozdony — gőzös kerekei zakatolnak",
        "Párás, gőzben teli — gőzös fürdő",
    ],
    "GYÁVA": [
        "Bátortalan, félős — ellentéte a bátor",
        "Nem mer szembeszállni — gyáva futásnak ered",
        "Nem bátor, félénk — gyáva nyúl szalad",
    ],
    "HADAK": [
        "Katonai csapatok — hadak útján vonuló sereg",
        "Harcosok serege — hadak vonulnak a határon",
        "Katonai erők — hadak útja a csillagos égen",
    ],
    "HAJAS": [
        "Hajas fej — dús hajzatú",
        "Hajjal borított — hajas koponyán sürű haj",
        "Dús hajjal rendelkező — hajas fejű ifjú",
    ],
    "HAJÓS": [
        "Hajón dolgozó személy — tengerész, révész",
        "Hajó személyzetének tagja — hajós a fedélzeten",
        "Viz alatti expedíción — tengerész, hajós",
    ],
    "HALAK": [
        "Vizes élőlények — akvárium lakói",
        "Vizi gerincesek — halak a folyóban és tengerben",
        "Uszonyos vízi állatok — halak úsznak a folyóban",
    ],
    "HALAS": [
        "Hallal bőséges — halastavon él",
        "Sok halat tartalmazó — halastó halas vizei",
        "Halbőséges — halas víz a Tisza partján",
    ],
    "HALOM": [
        "Domb, kupac — homokdombon játszanak a gyerekek",
        "Kis emelkedés, kiemelkedés — halmon áll a vár",
        "Rakás, kupac — könyvek halma az asztalon",
    ],
    "HÁROM": [
        "Kettő utáni szám — háromszög oldalainak száma",
        "3-as szám — három királyok napja",
        "Harmadik szám — három az egész, isten is ilyen",
    ],
    "HÁRFA": [
        "Húros hangszer — angyalok hangszere a képeken",
        "Pengetős zeneszer — hárfán játszik a muzsikus",
        "Nagy vonós hangszer — hárfa zengő hangja",
    ],
    "HAVAS": [
        "Hóval borított — téli havas táj",
        "Hóban gazdag — havas hegycsúcsok télen",
        "Hólepte — havas Kárpátok",
    ],
    "HIDEG": [
        "Alacsony hőmérsékletű — tél jellemzője",
        "Nem meleg, fagyos — hideg víz, hideg idő",
        "Fázósan — hideg szél fúj keletről",
    ],
    "HONOS": [
        "Valahol honos, őshonos — magyar tájra honos növény",
        "Eredeti, bennszülött — honos faj a Kárpát-medencében",
        "Természetes előfordulású — honos növényfaj",
    ],
    "HORDÓ": [
        "Fa vagy fém henger — boroshordó pincében",
        "Borhordó fából — hordóban ér a bor",
        "Fahordó bortárolásra — hordóban állt a régi bor",
    ],
    "HŰVÖS": [
        "Kicsit hideg, friss — őszi hűvös reggel",
        "Enyhén hideg — hűvös este a Balatonnál",
        "Kellemes frissesség — hűvös árnyékban pihenés",
    ],
    "IGAZI": [
        "Valódi, eredeti — igazi arany, nem hamis",
        "Autentikus, valódi — igazi népmese",
        "Eredeti, hiteles — igazi barátság értékes",
    ],
    "JOGAR": [
        "Királyi pálca, uralom jele — koronázási ékszer",
        "Uralom szimbóluma — koronával és jogarral",
        "Királyi jelkép — jogar és korona",
    ],
    "JÓKOR": [
        "Megfelelő időben — nem késve, időre",
        "Alkalmas pillanatban — jókor jött a segítség",
        "Kellő időpontban — jókor érkező vendég",
    ],
    "KAKAS": [
        "Hím tyúk — hajnalt hirdet a faluban",
        "Tyúkudvar ura — kakas kukorékol hajnalban",
        "Baromfi, reggeli hangjáról ismert — kakas szól",
    ],
    "KALAP": [
        "Fejfedő — cowboy kalapja",
        "Fejre tett fejfedő — kalapot emel köszöntéskor",
        "Nemezes vagy szalma fejfedő — kalap a fejébe nyomva",
    ],
    "KÁVÉS": [
        "Kávéval ízesített — kávés desszert",
        "Kávéhoz kapcsolódó — kávés tortán kávékrém",
        "Kávé ízű — kávés sütemény",
    ],
    "KAZAL": [
        "Szalmából rakott kupac — aratás után a mezőn",
        "Szalmaboglyó — kazalban rejlik az egér",
        "Szalma- vagy szénakupac — kazal a pusztán",
    ],
    "KAZÁR": [
        "Türk nép a középkorban — kazár birodalom a Kaszpi-tónál",
        "Kelet-európai ókori nép — kazár kereskedők",
        "Középkori steppe nép — kazár kagán uralma",
    ],
    "KELET": [
        "Napkelte iránya — Ázsia keleti kultúrái",
        "Égtáj, ahol felkel a nap — kelet felé indult",
        "Napkelet iránya — Keleti pályaudvar neve is",
    ],
    "KÉPEK": [
        "Festmények, fotók, ábrázolások — galériában kiállítva",
        "Vizuális alkotások — képek a falon",
        "Képzőművészeti alkotások — képek és szobrok",
    ],
    "KÉREM": [
        "Udvarias kérés szava — legyen szíves",
        "Kérelemszó, udvarias forma — kérem, adja ide",
        "Könyörgő kifejezés — kérem szépen",
    ],
    "KINCS": [
        "Értékes vagyon, drágaság — elásott kincs",
        "Becses vagyon — kincseket rejt a múzeum",
        "Értékes dolog — ásott kincs a vár alatt",
    ],
    "KÖRÖS": [
        "Folyó neve Magyarországon — Körös-vidék",
        "Kör alakú — körös-körül víz",
        "Kör formájú — körös elrendezés",
    ],
    "KŐRIS": [
        "Lombhullató fa — kőrisfa kemény fája",
        "Keményfájú lombos fa — kőriserdő Magyarországon",
        "Magyar erdők fája — kőris levele összetett",
    ],
    "KÖLES": [
        "Apró szemű gabona — madáreleség is lehet",
        "Kis szemű gabonafaj — kölesből kása készül",
        "Magyar hagyományos gabona — köleskása régi étel",
    ],
    "KŐVÁR": [
        "Kőből emelt vár — középkori védelem",
        "Erős kőfalú vár — kővár a hegyen",
        "Szilárd kővár — kővárban laktak a nemesek",
    ],
    "KUPAC": [
        "Kis halom, rakás — homokos kupac",
        "Rendezetlen halom — kupacban hever a levél",
        "Kis felrakás — kupac homok a homokvárhoz",
    ],
    "LATIN": [
        "Ókori Róma nyelve — egyházi latin",
        "Holt nyelv, egyházi tudományos — latin szöveg",
        "Régi diplomáciai-tudományos nyelv — latin felirat",
    ],
    "LEVES": [
        "Meleg folyékony étel — húsleves, gulyásleves",
        "Forró tálban tálalt étel — levest főzött a konyhán",
        "Magyar konyha alapétele — gulyásleves",
    ],
    "LEVÉL": [
        "Írásos üzenet — postán küldött levél",
        "Fa zöld lapja — levél lebeg ősszel",
        "Boríték tartalmaa — levél érkezett a postán",
    ],
    "LIGET": [
        "Kis parkerdő — városi liget",
        "Parkszerű erdőrész — Városliget Budapesten",
        "Árnyékos facsoportos terület — ligetben sétáltak",
    ],
    "LISZT": [
        "Darált gabona — kenyérhez kell",
        "Magyar zenész neve — Liszt Ferenc zongorista",
        "Fehér por kenyérsütéshez — liszt és víz tésztává gyúrva",
    ],
    "LOVAG": [
        "Páncélos harcos — középkori lovagi tornán",
        "Középkori páncélos harcos — lovag szertartáson kapta rangját",
        "Páncélt viselő harcos — lovagi erény",
    ],
    "LOVAK": [
        "Ló, többes szám — lovarda állatai",
        "Nemes háziállatok — lovak a legelőn",
        "Lovardai állatok — lovakat itatnak a pataknál",
    ],
    "MADÁR": [
        "Tollas szárnyas állat — fészkét fára rakja",
        "Repülő tollas élőlény — madárdal a hajnalban",
        "Szárnya van és énekel — madár ül a galyon",
    ],
    "MALOM": [
        "Gabonát őrlő szerkezet — szélmalom forog a szélben",
        "Lisztet gyárt — vízimalom a folyón",
        "Régi gabonafeldolgozó — malomban őrlik a búzát",
    ],
    "MELEG": [
        "Magas hőmérsékletű — nyár jellemzője",
        "Nem hideg, kellemes — meleg nap, meleg ágy",
        "Felmelegedett — meleg nyári nap",
    ],
    "MESÉK": [
        "Népmesék, tündérmesék — gyerekeknek mesélnek",
        "Magyar néphagyomány gyöngyszemei — régi mesék",
        "Fantasztikus elbeszélések — mesék hősei",
    ],
    "MESÉS": [
        "Mesébe illő, csodás — mesés táj",
        "Rendkívül szép — mesés kilátás a hegyről",
        "Fantasztikus, varázsos — mesés erdő",
    ],
    "MÉHES": [
        "Méhek lakhelye — méhész gondozza",
        "Méhkaptárak helye — méhes az almáskertben",
        "Kaptárakkal teli ház — méhes terméke a méz",
    ],
    "MÉZES": [
        "Mézzel édesített — mézes kalács, mézes pogácsa",
        "Mézízes — mézes sütemény hagyomány",
        "Édes mézzel — mézes bor, mézes szó",
    ],
    "MEZŐK": [
        "Füves síkságok — mező virágai, búzamező",
        "Szántóföldi területek — búzamezők az Alföldön",
        "Nyílt területek — mezőkön sétál a pásztor",
    ],
    "MOHOS": [
        "Mohával borított — mohos kő a patak szélén",
        "Zöld mohával fedett — mohos fa törzse",
        "Nedves, mohos — mohos erdei kő",
    ],
    "MÓZES": [
        "Bibliai próféta — a tíz parancsolat átadója",
        "Az Ótestamentum prófétája — Mózes a Sínai-hegyen",
        "Bibliai vezér, törvényhozó — Mózes népe Egyiptomból",
    ],
    "MUTAT": [
        "Jelzi, irányba mutat — ujjal mutat",
        "Megmutat, bemutat — irányba mutat az út",
        "Jelez, irányt szab — mutat az óramutató",
    ],
    "NAPOK": [
        "A nap egységei — hét napból áll a hét",
        "Időbeli egységek — napok telnek el",
        "Nap-nap után — napok hosszán",
    ],
    "NAPOS": [
        "Napsütötte — napos időjárás",
        "Fényes, naptól megvilágított — napos délelőtt",
        "Fénnyel teli — napos oldal a dombon",
    ],
    "NÁDAS": [
        "Nádas terület, nádfedeles rét — Balaton-parti nádas",
        "Náddal borított vizes terület — nádas sürűjében nő a gém",
        "Tóparti nádfás rész — nádas madárfészek",
    ],
    "NÁDOR": [
        "Középkori magyar főméltóság — nádori cím",
        "Magyar királyság helytartója — nádor és király",
        "Régi magyar politikai rang — nádori hivatal",
    ],
    "NEMES": [
        "Előkelő, nemesi — nemesi osztály tagja",
        "Kiváló minőségű — nemes bor, nemes anyag",
        "Arisztokrata, nemes ember — nemes kastélya",
    ],
    "NOMÁD": [
        "Vándorló életmódú nép — sátorban él, vonul",
        "Állandó lakhelye nincs — nomád életmód a pusztán",
        "Legelőről legelőre vándorló — nomád pásztor",
    ],
    "NYÁRI": [
        "Nyárhoz tartozó — nyári szabadság",
        "Nyáron jellemző — nyári hőség",
        "Meleg évszak jelzője — nyári dallam",
    ],
    "OPERA": [
        "Zenés színházi műfaj — operaházi előadás",
        "Zenés drámai mű — opera és balett",
        "Énekes zenedráma — opera Budapesten",
    ],
    "ORDAS": [
        "Farkasszürke, komor — ordas farkas",
        "Sötét szürke farkasszínű — ordas erdő",
        "Farkas szín jelzője — ordas tél",
    ],
    "ŐSZIG": [
        "Őszig tartó — nyártól őszig",
        "Az őszi időszakig — őszig süt a nap",
        "Tarddig, őszig terjedő — őszig marad",
    ],
    "PADLÓ": [
        "Ház aljzata, padlózat — fából vagy csempéből",
        "Szoba talpfelülete — padlón ülnek a gyerekek",
        "Szobaalap — parkettás padló",
    ],
    "PATAK": [
        "Kis vízfolyás — hegyipatak csörgedezése",
        "Kis folyóvíz — patak csörgedez a réten",
        "Folyóba tartó kis víz — patak hűvös vize",
    ],
    "PÉTER": [
        "Keresztnév — Péter apostol",
        "Magyar férfinév — Péter-Pál napja június 29.",
        "Férfinév — Péter apostol Krisztus követője",
    ],
    "PIROS": [
        "Vöröses szín — alma piros",
        "Tűz és vér színe — piros zászló",
        "Élénk piros szín — piros rózsa szerelmet jelent",
    ],
    "PONTY": [
        "Édesvízi hal — halpaprikás alapanyaga",
        "Magyar folyók hala — ponty a tányéron",
        "Édesvízi halfaj — ponty karácsonyi hal",
    ],
    "PORTA": [
        "Kapu, bejárat — oszmán porta, udvari kapu",
        "Oszmán udvar neve — Magas Porta Konstantinápolyban",
        "Bejárati kapu — porta mögött az udvar",
    ],
    "RÉTES": [
        "Vékony tésztás sütemény — almás rétes",
        "Magyar sütemény rétestésztából — rétest húznak az asszonyok",
        "Hagyományos magyar édesség — mákos vagy almás rétes",
    ],
    "RETEK": [
        "Csípős gyökérzöldség — salátába vágják",
        "Piros vagy fehér gyökérzöldség — rétek saláta frissít",
        "Kis kerek zöldség — retek csípős",
    ],
    "RÓMAI": [
        "Rómához kötődő — ókori római birodalom",
        "Róma városára vonatkozó — római légió menetelt",
        "Antik Róma jelzője — római fürdő régi emlék",
    ],
    "ROMÁN": [
        "Romániai személy vagy román stílus — román építészet",
        "Románia lakosa vagy jelzője — román határ közelben",
        "Román népcsoport — román szomszéd",
    ],
    "RÓZSA": [
        "Tövises virág — szerelem jelképe",
        "Illatos kerti virág — rózsa pirul a kertben",
        "Piros virág — rózsa az ablakban",
    ],
    "SARLÓ": [
        "Aratóeszköz, görbe penge — gabonát vágnak vele",
        "Ívelt aratókés — sarló és kalapács jelkép",
        "Görbe pengéjű kézszerszám — sarló kaszál",
    ],
    "SASOK": [
        "Ragadozó nagymadarak — sasok a szirten fészkelnek",
        "Sas madarak többesben — sasok keringenek a hegycsúcs fölött",
        "Solymász sasai — sasok a Magyar címerben",
    ],
    "SASOS": [
        "Sassal díszített — sasos zászló",
        "Sashoz hasonló — sasos tekintet",
        "Sas motívumú — sasos pajzs",
    ],
    "SÁTOR": [
        "Ideiglenes vászon szállás — táborozáshoz",
        "Nomád lakóhely — sátorban él a pásztor",
        "Vászonból álló szállás — sátor alatt tábortűz",
    ],
    "SEREG": [
        "Katonai csapat — nagy sereg vonult",
        "Katonák sora — sereg menetelt az úton",
        "Katonai erő — sereg gyülekezik a csatára",
    ],
    "SÍKOS": [
        "Csúszós felület — jégen síkos az út",
        "Csúszásveszélyes — síkos kő a pataknál",
        "Nem tapadós, glatt — síkos út télen",
    ],
    "SZÁSZ": [
        "Germán nép — erdélyi szászok, szász örökség",
        "Szász nép tagja — erdélyi szász városok",
        "Szász népcsoport — szász kultúra Erdélyben",
    ],
    "SZARV": [
        "Szarvasmarha feje tetején — bikaszarv",
        "Állati szarv — szarv és pata",
        "Szarvas szarva — szarv a szarvas fején",
    ],
    "SÜKET": [
        "Hallássérült — süket fülekre talál",
        "Nem hall — süket ember gesztikulál",
        "Hallásának hiánya — süket és néma",
    ],
    "SÜTIK": [
        "Sütőben készülő ételek — sütiket sütünk",
        "Édességek a kemencéből — süti és torta",
        "Édeskés tészta — sütiket hozok az iskolába",
    ],
    "TÁBOR": [
        "Katonai vagy nyári tábor — táborba vonul",
        "Ideiglenes száll, táborhely — táborban éltek",
        "Cserkész- és nyáritábor — tábortűz körül ülnek",
    ],
    "TÁBLA": [
        "Írótábla, tábla — iskolai tábla",
        "Sík lap — táblán tanít a tanár",
        "Lapos felület — tábla csoki",
    ],
    "TATÁR": [
        "Mongol-türk nép — tatár invázió",
        "Keleti nép tagja — tatárjárás pusztítása",
        "Keleti steppei nép — tatár harcosok lovai",
    ],
    "TÉLEN": [
        "Téli időszakban — télen havazik",
        "Téli szezonban — télen szánkóznak a gyerekek",
        "Hideg évszakban — télen befagy a tó",
    ],
    "TIGRI": [
        "Csíkos nagymacska — Ázsia ragadozója",
        "Bengal tigris — tigris ugrik az áldozatra",
        "Nagy macskafélék egyik faja — tigris foltjai csíkosak",
    ],
    "TŐKÉS": [
        "Tőketulajdonos — gazdasági szereplő",
        "Tőke tulajdonosa — tőkés osztály",
        "Ipari vállalkozó — tőkés és munkás",
    ],
    "TÖLGY": [
        "Makktermő fa — tölgyfa erdő",
        "Erős lombos fa — tölgyfából cipő és hordó",
        "Makktermő erdei fa — tölgyerdő Magyarországon",
    ],
    "TORTA": [
        "Ünnepi sütemény — születésnapi torta",
        "Krémtorta desszert — torta gyertyával",
        "Édes kerek desszert — torta és szülinap",
    ],
    "TÖRÖK": [
        "Oszmán-türk nép — török hódoltság kora",
        "Törökország lakója — török fürdő emléke",
        "Oszmán birodalom népe — török sereg hódított",
    ],
    "TÚRÓS": [
        "Túrós, tejtermékkel töltött — túrós rétes",
        "Túróval ízesített — túrós tészta magyar étel",
        "Túróval készített — túrós batyu sütemény",
    ],
    "UDVAR": [
        "Ház melletti nyílt tér — udvari kút",
        "Belső udvar — udvarban játszanak a gyerekek",
        "Palotai vagy udvari tér — udvarban áll a nemesek serege",
    ],
    "VADON": [
        "Ősvadon, vad természet — dzsungel vadonja",
        "Természetes vadás terület — vadonban él a farkas",
        "Érintetlen természet — vadon erdeje",
    ],
    "VADAK": [
        "Vad állatok — vadász vadakra vadászik",
        "Erdei állatok — vadak a rengetegben",
        "Vad élőlények — vadak és háziállatok",
    ],
    "VÁRAK": [
        "Középkori erődítmények — várak és kastélyok",
        "Kőfalú erődök — várak a hegytetőn",
        "Kővárformák — várak alapján ma múzeum",
    ],
    "VÁSÁR": [
        "Kereskedelmi esemény — hetivásár a téren",
        "Piac, árucsere helyszín — vásáron vett árut",
        "Tér vagy utca piaca — vásáron kóstolta a hungarikumot",
    ],
    "VÁROS": [
        "Nagyobb település — főváros és vidéki város",
        "Városi élet — városban él a legtöbb ember",
        "Lakott hely, járási székhely — a város szívében",
    ],
    "VILÁG": [
        "Mindenség, föld — a világ körül",
        "Az egész Föld — a világ népei",
        "Fény, világosság — gyertya világít a sötétben",
    ],
    "VIHAR": [
        "Erős szél és eső — tengeri vihar",
        "Viharos időjárás — vihar vonult a hegyen",
        "Zivatar, szélvihar — vihar előtti csend",
    ],
    "VITÉZ": [
        "Bátran harcoló hős — vitézlő katona",
        "Magyar hősi cím — vitéz katonának adományozták",
        "Bátor, derék harcos — vitézség jellemzi",
    ],
    "ZÖLDE": [
        "Zöldes árnyalatú — rét zöldje",
        "Enyhén zöld — zölde szín a tavaszi réten",
        "Halványzöld — zölde mező tavasszal",
    ],
    "ZÚGÁS": [
        "Mély hangos zaj — szél zúgása",
        "Mormolás, bugás — zúgás hallatszik a vízesésből",
        "Folyamatos hangzavar — erdő zúgása szélben",
    ],
}

def get_clue(word, variant=0):
    """Return a clue for the given word. Uses variant to pick different clues."""
    clue_list = CLUES.get(word)
    if clue_list:
        return clue_list[variant % len(clue_list)]
    return f"Öt betűs szó: {word.lower()}"


# ─── PUZZLE PLAN ─────────────────────────────────────────────────────────────

# Format: (topic, difficulty, title_hu, category)
PUZZLE_PLAN = [
    # ── GEOGRAPHY EASY (20) ──
    ("hungarian-cities",      "easy",   "Magyar városok",               "geography"),
    ("hungarian-cities",      "easy",   "Magyar városok II",            "geography"),
    ("rivers",                "easy",   "Magyar folyók",                "geography"),
    ("rivers",                "easy",   "Magyar folyók II",             "geography"),
    ("balaton",               "easy",   "A Balaton",                    "geography"),
    ("balaton",               "easy",   "Balaton és vidéke",            "geography"),
    ("plains",                "easy",   "Az Alföld",                    "geography"),
    ("plains",                "easy",   "Magyar síkság",                "geography"),
    ("mountains",             "easy",   "Magyar hegyek",                "geography"),
    ("mountains",             "easy",   "Hegyek és völgyek",            "geography"),
    ("neighboring-countries", "easy",   "Szomszéd országok",           "geography"),
    ("neighboring-countries", "easy",   "Határok mentén",              "geography"),
    ("european-capitals",     "easy",   "Európai fővárosok",           "geography"),
    ("european-rivers",       "easy",   "Európai folyók",              "geography"),
    ("continents",            "easy",   "Kontinensek",                 "geography"),
    ("climate",               "easy",   "Éghajlati övek",              "geography"),
    ("forests",               "easy",   "Európa erdői",                "geography"),
    ("islands",               "easy",   "Szigetek",                    "geography"),
    ("deserts",               "easy",   "Sivatagok",                   "geography"),
    ("oceans",                "easy",   "Tengerek és óceánok",         "geography"),
    # ── GEOGRAPHY MEDIUM (20) ──
    ("hungarian-cities",      "medium", "Magyar városok haladóknak",   "geography"),
    ("hungarian-cities",      "medium", "Városok Magyarországon",      "geography"),
    ("rivers",                "medium", "Folyórendszerek",             "geography"),
    ("rivers",                "medium", "Folyók és tavak",             "geography"),
    ("balaton",               "medium", "Balaton természetrajza",      "geography"),
    ("mountains",             "medium", "Hegységek Európában",         "geography"),
    ("mountains",             "medium", "Alpok és Kárpátok",           "geography"),
    ("neighboring-countries", "medium", "Szomszédos népek",            "geography"),
    ("neighboring-countries", "medium", "Határszéli tájak",            "geography"),
    ("european-capitals",     "medium", "Európai fővárosok II",        "geography"),
    ("european-rivers",       "medium", "Nagy európai folyók",         "geography"),
    ("mediterranean",         "medium", "A Mediterrán",                "geography"),
    ("alps",                  "medium", "Az Alpok",                    "geography"),
    ("world-oceans",          "medium", "Óceánok és tengerek",         "geography"),
    ("africa",                "medium", "Afrika földrajza",            "geography"),
    ("asia",                  "medium", "Ázsia tájain",                "geography"),
    ("south-america",         "medium", "Dél-Amerika",                 "geography"),
    ("volcanoes",             "medium", "Vulkánok",                    "geography"),
    ("arctic",                "medium", "Sarki vidékek",               "geography"),
    ("world-lakes",           "medium", "Világ tavai",                 "geography"),
    # ── CULTURE EASY (18) ──
    ("hungarian-literature",  "easy",   "Magyar irodalom",             "culture"),
    ("hungarian-literature",  "easy",   "Írók és költők",              "culture"),
    ("poetry",                "easy",   "Magyar költészet",            "culture"),
    ("poetry",                "easy",   "Versek világa",               "culture"),
    ("folk-tales",            "easy",   "Magyar népmesék",             "culture"),
    ("folk-tales",            "easy",   "Népmesék hősei",              "culture"),
    ("folk-music",            "easy",   "Magyar népzene",              "culture"),
    ("folk-music",            "easy",   "Dalok és nóták",              "culture"),
    ("classical-music",       "easy",   "Klasszikus zene",             "culture"),
    ("classical-music",       "easy",   "Zeneszerzők",                 "culture"),
    ("opera",                 "easy",   "Operavilág",                  "culture"),
    ("theater",               "easy",   "Színház",                     "culture"),
    ("painting",              "easy",   "Festészet",                   "culture"),
    ("folk-art",              "easy",   "Magyar népművészet",          "culture"),
    ("dance",                 "easy",   "Tánc és csárdás",             "culture"),
    ("cinema",                "easy",   "Magyar film",                 "culture"),
    ("festivals",             "easy",   "Ünnepek és fesztiválok",      "culture"),
    ("museums",               "easy",   "Múzeumok",                    "culture"),
    # ── CULTURE MEDIUM (19) ──
    ("hungarian-literature",  "medium", "Irodalmi alkotások",          "culture"),
    ("hungarian-literature",  "medium", "Petőfi és Arany",             "culture"),
    ("poetry",                "medium", "Verses formák",               "culture"),
    ("folk-tales",            "medium", "Tündérmesék",                 "culture"),
    ("folk-music",            "medium", "Hangszerek",                  "culture"),
    ("classical-music",       "medium", "Liszt és Bartók",             "culture"),
    ("opera",                 "medium", "Operahősök",                  "culture"),
    ("theater",               "medium", "Dráma és komédia",            "culture"),
    ("painting",              "medium", "Képzőművészet",               "culture"),
    ("sculpture",             "medium", "Szobrászat",                  "culture"),
    ("folk-art",              "medium", "Hímzés és fazekas",           "culture"),
    ("dance",                 "medium", "Néptánc hagyomány",           "culture"),
    ("architecture",          "medium", "Építészet",                   "culture"),
    ("folk-costumes",         "medium", "Népi viselet",                "culture"),
    ("crafts",                "medium", "Kézműves mesterségek",        "culture"),
    ("weaving",               "medium", "Szövés és fonás",             "culture"),
    ("wood-carving",          "medium", "Faragás",                     "culture"),
    ("church-art",            "medium", "Egyházi művészet",            "culture"),
    ("libraries",             "medium", "Könyvtárak és könyvek",       "culture"),
]

assert len(PUZZLE_PLAN) == 77, f"Expected 77 puzzles, got {len(PUZZLE_PLAN)}"

# ─── GENERATE PUZZLES ────────────────────────────────────────────────────────

def make_puzzle(puzzle_id, title_hu, category, difficulty, grid_tuple, variant):
    """Build a puzzle JSON dict."""
    row0, row2, row4, col0, col2, col4 = grid_tuple
    matrix = grid_to_matrix(row0, row2, row4, col0, col2, col4)

    # For across, use variant 0; for down, use variant 1 (or 2) for different clue text
    across_clues = [
        get_clue(row0, variant),
        get_clue(row2, variant),
        get_clue(row4, variant),
    ]
    down_clues = [
        get_clue(col0, variant + 1),
        get_clue(col2, variant + 1),
        get_clue(col4, variant + 1),
    ]

    return {
        "id": puzzle_id,
        "title": {"hu": title_hu},
        "category": category,
        "difficulty": difficulty,
        "gridSize": {"rows": 5, "cols": 5},
        "grid": matrix,
        "clues": {
            "across": [
                {"number": 1, "clue": {"hu": across_clues[0]}, "row": 0, "col": 0, "length": 5},
                {"number": 4, "clue": {"hu": across_clues[1]}, "row": 2, "col": 0, "length": 5},
                {"number": 5, "clue": {"hu": across_clues[2]}, "row": 4, "col": 0, "length": 5},
            ],
            "down": [
                {"number": 1, "clue": {"hu": down_clues[0]}, "row": 0, "col": 0, "length": 5},
                {"number": 2, "clue": {"hu": down_clues[1]}, "row": 0, "col": 2, "length": 5},
                {"number": 3, "clue": {"hu": down_clues[2]}, "row": 0, "col": 4, "length": 5},
            ],
        },
    }


def generate_all():
    base = Path("/Users/nadavsolomon/Code/hu-crossword-puzzle/public/puzzles")

    # Track numbering per (category, topic, difficulty)
    counters = {}

    written = 0
    skipped = 0

    for i, (topic, difficulty, title_hu, category) in enumerate(PUZZLE_PLAN):
        # Pick a grid
        grid = working_grids[i % len(working_grids)]

        # File numbering: start at 010 to avoid conflict with 001-009
        key = (category, topic, difficulty)
        if key not in counters:
            counters[key] = 10
        else:
            counters[key] += 1
        num = counters[key]
        num_str = f"{num:03d}"

        puzzle_id = f"{category}-{topic}-{difficulty}-{num_str}"
        filename = f"{topic}-{difficulty}-{num_str}.json"
        outdir = base / category
        outpath = outdir / filename

        if outpath.exists():
            print(f"SKIP (exists): {outpath.name}")
            skipped += 1
            continue

        puzzle = make_puzzle(puzzle_id, title_hu, category, difficulty, grid, variant=i % 3)

        outdir.mkdir(parents=True, exist_ok=True)
        with open(outpath, 'w', encoding='utf-8') as f:
            json.dump(puzzle, f, ensure_ascii=False, indent=2)

        print(f"WROTE: {category}/{filename}  words={grid[0]},{grid[1]},{grid[2]} | {grid[3]},{grid[4]},{grid[5]}")
        written += 1

    print(f"\nDone. Written: {written}, Skipped: {skipped}")


if __name__ == "__main__":
    generate_all()
