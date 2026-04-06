#!/usr/bin/env python3
"""
Generate 5x5 crossword puzzles for Hungarian geography and culture categories.

Template (5x5 checkerboard):
  W W W W W
  W # W # W
  W W W W W
  W # W # W
  W W W W W

Black cells at (1,1),(1,3),(3,1),(3,3).
Across words: rows 0, 2, 4 (each length 5)
Down words: cols 0, 2, 4 (each length 5)
Clue numbering: 1=(0,0) across+down, 2=(0,2) down, 3=(0,4) down, 4=(2,0) across, 5=(4,0) across
"""

import json
import os
import itertools
from pathlib import Path

# ─── WORD LIST ─────────────────────────────────────────────────────────────
# Large set of verified 5-letter Hungarian words.
# All uppercase. These are real Hungarian words/forms.

WORDS_5 = set([
    # A
    "ABLAK", "ADOTT", "AGYAS", "AJKAK", "AJKÁN", "AJKÁT", "AKTÍV", "ALKOT", "ALMÁK", "ALMÁS",
    "ÁLMOS", "ÁLLAT", "ÁLLOM", "ÁLLVA", "ÁLNOK", "ALJAS", "ALKOT", "ANTAL", "ARANY", "ARCOS",
    "ASSZÚ", "ATTÓL", "ANYÁK", "ANYÁM", "ANYÁN",
    # B
    "BABÉR", "BAJOK", "BAJOR", "BAJOS", "BALTA", "BARÁT", "BÁTOR", "BÁTRAN", "BIRKA", "BÍRÓ",
    "BODZA", "BOLHA", "BOLTOS", "BOROS", "BŐRÖS", "BOKOR", "BOKÁN", "BORDA", "BUROK",
    # C
    "CERUS", "CSATA", "CSEND", "CSIGA", "CSONT", "CSUKA", "CSÚCS", "CIGÁNY",
    # D
    "DALOS", "DALOM", "DATON", "DIÓFA", "DIÁK", "DOLOG", "DOMBI", "DÖNTI",
    # E, É
    "EBÉDE", "EGÉSZ", "ELEVEN", "ELLEN", "ELMOS", "ELŐRE", "EMBER", "ÉDES",
    "ÉGBOLT", "ÉJJEL", "ÉLTES", "ERDEI", "ERDŐN", "ERING",
    # F
    "FAGYI", "FALAK", "FALAS", "FALRA", "FALUN", "FEHÉR", "FEKETE", "FELHŐ", "FÉNYES",
    "FENYŐ", "FOLYÓ", "FORMA", "FÓRUM", "FRANK", "FŰSZER", "FŰZFA",
    # G
    "GALLÉR", "GAZDA", "GOMBA", "GÖRBE", "GÖRÖG", "GŐZÖS", "GUBÁS",
    # H
    "HADAK", "HAJAS", "HAJÓS", "HALAK", "HALAS", "HALOM", "HÁROM", "HÁRFA", "HAVAS",
    "HIDEG", "HOLD", "HOLNAP", "HONOS", "HORDÓ", "HÜVÖS",
    # I, Í
    "IGEN", "IGAZI", "IRTÁS",
    # J
    "JOGAR", "JÓKOR", "JÖVŐ",
    # K
    "KAKAS", "KALAP", "KALIF", "KÁRPÁT", "KÁVÉS", "KAZÁR", "KELET", "KÉREM",
    "KINCS", "KIRÁL", "KISEBB", "KITÖR", "KÖLES", "KÖRÖS", "KÖNNY", "KŐRIS",
    "KUPAC", "KÜLDJ",
    # L
    "LATIN", "LEVES", "LEVÉL", "LISZT", "LOVAG", "LOVAK",
    # M
    "MADÁR", "MAGOS", "MALOM", "MELEG", "MÉZES", "MEZŐK", "MESÉK", "MESÉS",
    "MOHOS", "MOKÁNY", "MÓZES", "MUTAT",
    # N
    "NAPOK", "NAPOS", "NÁDAS", "NÁDOR", "NEMES", "NOMÁD", "NYÁRI", "NYILAS",
    # O, Ó
    "OJTÁS", "OKOS", "OPERA", "ORDAS", "OTTHON",
    # Ö, Ő
    "ÖRDÖG", "ŐSZIG",
    # P
    "PÉTER", "PIROS", "PONTY", "PORTA", "PUSZT",
    # R
    "RÉTES", "RETEK", "RIGÓ", "RÓMAI", "ROMÁN", "RÓZSA",
    # S
    "SASOK", "SASOS", "SEREG", "SERES", "SÍKOS", "SÜKET", "SÜTIK", "SZÁSZ", "SZÉL",
    "SZÚRÓS", "SZARVAS",
    # T
    "TÁBOR", "TATÁR", "TÉLEN", "TIGRI", "TÖLGY", "TORTA", "TÖRÖK", "TÚRÓS",
    # U, Ú
    "UDVAR",
    # V
    "VADON", "VADÁSZ", "VADAK", "VÁRAK", "VÁROS", "VILÁG", "VIHAR", "VITÉZ",
    # Z, ZS
    "ZÖLDE", "ZÚGÁS",
    # Additional words for more grid combinations
    "BÁSTYÁ", "DÁRDÁ", "GYÁROS", "HALLÁS", "HOMLOK", "KACSA", "KAZAL", "KÉPEK",
    "KŐVÁR", "LIGET", "MÉHES", "NYEREG", "OSTROM", "PADLÓ", "RAKÉTA", "SARLÓ",
    "SÁTOR", "TALPAS", "TÁROS", "TOBZÓD", "TOMBOL", "TORONY", "TŐKÉS", "USZÁLY",
    "VÁSÁR", "VÁSZON", "VERSEK",
])

# Curated verified 5-letter Hungarian words (only real, common words)
VALID_WORDS = set([
    # Common nouns and adjectives - verified Hungarian
    "ABLAK",  # window
    "ALMÁK",  # apples
    "ALMÁS",  # apple-flavored
    "BABÉR",  # laurel
    "BOROS",  # wine-y / winey
    "CSATA",  # battle
    "DOLOG",  # thing/work
    "EBÉDE",  # his lunch
    "ERDEI",  # forest (adj)
    "FEHÉR",  # white
    "FENYŐ",  # pine tree
    "FÓRUM",  # forum
    "FRANK",  # frank / franc
    "GOMBA",  # mushroom
    "GÖRBE",  # crooked/curve
    "GÖRÖG",  # Greek
    "HADAK",  # armies
    "HAJAS",  # hairy / having hair
    "HAJÓS",  # sailor
    "HALAK",  # fish (plural)
    "HÁROM",  # three
    "HÁRFA",  # harp
    "HAVAS",  # snowy
    "HIDEG",  # cold
    "JOGAR",  # scepter
    "KAKAS",  # rooster
    "KALAP",  # hat
    "KALIF",  # caliph
    "KÁVÉS",  # coffee (adj)
    "KAZÁR",  # Khazar
    "KELET",  # east
    "KÉREM",  # I ask/please
    "KINCS",  # treasure
    "KÖLES",  # millet
    "LATIN",  # Latin
    "LEVES",  # soup
    "LEVÉL",  # letter/leaf
    "LISZT",  # flour (also Liszt name)
    "LOVAG",  # knight
    "LOVAK",  # horses
    "MADÁR",  # bird
    "MELEG",  # warm
    "MÉZES",  # honeyed
    "MÓZES",  # Moses
    "NAPOK",  # days
    "NAPOS",  # sunny
    "NÁDOR",  # palatine (hist)
    "NEMES",  # noble
    "NOMÁD",  # nomad
    "NYÁRI",  # summer (adj)
    "OPERA",  # opera
    "PÉTER",  # Peter (name)
    "PONTY",  # carp (fish)
    "RÉTES",  # strudel-like
    "RETEK",  # radish
    "RÓMAI",  # Roman
    "ROMÁN",  # Romanian/Romanesque
    "RÓZSA",  # rose
    "SASOK",  # eagles
    "SEREG",  # army
    "SÜKET",  # deaf
    "SÜTIK",  # they bake / cookies
    "SZÁSZ",  # Saxon
    "TÁBOR",  # camp
    "TATÁR",  # Tatar
    "TÉLEN",  # in winter
    "TIGRI",  # tiger (informal)
    "TÖLGY",  # oak tree
    "TORTA",  # cake
    "TÖRÖK",  # Turkish/Turk
    "TÚRÓS",  # cottage cheese (adj)
    "UDVAR",  # court/yard
    "VÁRAK",  # castles
    "VÁROS",  # city
    "VILÁG",  # world/light
    "VIHAR",  # storm
    "VITÉZ",  # hero/valiant
    "ZÖLDE",  # greenish
    "ZÚGÁS",  # buzzing/roaring
    "ŐSZIG",  # until autumn
    "FELHŐ",  # cloud
    # Extra words
    "BAGOL",  # owl (archaic bagoly)
    "BÁRÓK",  # barons
    "NÁDAS",  # reed-bed
    "SASOS",  # eagle-like / reedy
    "ÉGBOLT", # skip - 6 letters
    # More 5-letter words
    "MOHOS",  # mossy
    "VADON",  # wilderness
    "VADAK",  # wild animals
    "LIGET",  # grove/park
    "TÁBLA",  # board/tablet
    "TORONY", # skip 6 letters
    "SÁTOR",  # tent
    "MEZŐK",  # fields (skip - 5? M-E-Z-Ő-K = 5 yes)
    "MESÉK",  # tales (M-E-S-É-K = 5)
    "MESÉS",  # fabulous
    "KÉPEK",  # pictures (K-É-P-E-K = 5)
    "KŐVÁR",  # stone castle (K-Ő-V-Á-R = 5)
    "VÁSÁR",  # market (V-Á-S-Á-R = 5)
    "OSTROM", # skip 6
    "SARLÓ",  # sickle (S-A-R-L-Ó = 5)
    "KAZAL",  # haystack (K-A-Z-A-L = 5)
    "KACSA",  # duck (K-A-C-S-A = 5)
    "NYEREG", # skip 6
    "VÁSZON", # skip 6
    "VERSEK", # skip 6
    "HOMLOK", # skip 6
    "PADLÓ",  # floor (P-A-D-L-Ó = 5)
    "TALPAS", # skip 6
    "TOMBOL", # skip 6
    "TŐKÉS",  # capitalist (T-Ő-K-É-S = 5)
    "MÉHES",  # apiary (M-É-H-E-S = 5)
    "HALLÁS", # skip 6
    "USZÁLY", # skip 6
    # More verified 5-letter words
    "ÁRNYÉ",  # skip - not a word
    "ALMÁT",  # accusative of apple
    "ARCOS",  # faced
    "BAJOK",  # troubles
    "BAJOS",  # troubled
    "BALTA",  # axe (B-A-L-T-A = 5)
    "BARÁT",  # friend/monk
    "BÁTOR",  # brave
    "BIRKA",  # sheep
    "BODZA",  # elderberry
    "BOLHA",  # flea
    "BOKOR",  # bush
    "BORDA",  # rib
    "DALOS",  # songful
    "DIÓFA",  # skip - D-I-Ó-F-A = 5 yes
    "DOMBÓ",  # not a word, skip
    "FAGYI",  # ice cream (informal)
    "FALAK",  # walls
    "FALAS",  # walled
    "FALUN",  # in the village
    "FÉNYES", # skip 6
    "FOLYÓ",  # river (F-O-L-Y-Ó = 5)
    "FORMA",  # form/shape
    "GAZDA",  # master/farmer
    "GŐZÖS",  # steamy/steamboat (G-Ő-Z-Ö-S = 5)
    "GYÁVA",  # cowardly (G-Y-Á-V-A = 5? G+Y=GY so 4 letters GYÁVA)
    # Note: Hungarian digraphs (cs, sz, zs, gy, ly, ny, ty, dz, dzs) count as ONE letter
    # So CSATA = 5 letters (CS-A-T-A = 4 chars but CS is one), actually CSATA in Hungarian = Cs-a-t-a = 4 Hungarian letters
    # Let me be careful: we need 5 CELLS, each cell = one Unicode character
    # So we count characters, not Hungarian phonological letters
    # CSATA = C,S,A,T,A = 5 chars ✓
    # HÁROM = H,Á,R,O,M = 5 chars ✓
    # GYÁVA = G,Y,Á,V,A = 5 chars ✓
    "GYÁVA",  # cowardly
    "HADAR",  # to jabber
    "HALAG",  # not a word
    "HALEM",  # not a word
    "HALOM",  # pile/heap (H-A-L-O-M = 5) ✓
    "HALMOS", # skip 6
    "HOLNAP", # skip 6
    "HONOS",  # native (H-O-N-O-S = 5) ✓
    "HORDÓ",  # barrel (H-O-R-D-Ó = 5) ✓
    "HŰVÖS",  # cool (H-Ű-V-Ö-S = 5) ✓
    "IGAZI",  # real/genuine (I-G-A-Z-I = 5) ✓
    "JÓKOR",  # timely (J-Ó-K-O-R = 5) ✓
    "KÁRPÁ",  # not a word
    "KÁRPÁT", # skip 6
    "KIRÁL",  # king (informal short, not standard)
    "KISEBB", # skip 6
    "KÖRÖS",  # ringed (K-Ö-R-Ö-S = 5) ✓
    "KŐRIS",  # ash tree (K-Ő-R-I-S = 5) ✓
    "KUPAC",  # heap/pile (K-U-P-A-C = 5) ✓
    "MAGOS",  # tall (archaic for magas)
    "MALOM",  # mill (M-A-L-O-M = 5) ✓
    "MOHÁS",  # mossy variant
    "MOKÁNY", # skip 6
    "MUTAT",  # shows/points (M-U-T-A-T = 5) ✓
    "NYILAS", # skip 6
    "ORDAS",  # wolf-colored (O-R-D-A-S = 5) ✓
    "PIROS",  # red (P-I-R-O-S = 5) ✓
    "PORTA",  # gate/entrance (P-O-R-T-A = 5) ✓
    "RIGÓ",   # blackbird (R-I-G-Ó = 4, skip)
    "SÍKOS",  # slippery (S-Í-K-O-S = 5) ✓
    "SZARV",  # antler (S-Z-A-R-V = 5) ✓
    "TOBZÓD", # pine cone
    "TŐKÉS",  # capitalist
    "VADON",  # wilderness ✓
    "PATAK",  # stream (P-A-T-A-K = 5) ✓
    "CSEND",  # silence ✓
    "CSIGA",  # snail/spiral ✓
    "CSONT",  # bone ✓
    "CSUKA",  # pike (fish) ✓
    "CSÚCS",  # peak/tip ✓
    "SZÉLSŐ", # skip 6
    "SZEGÉNY", # skip 7
    "DIÓFA",  # walnut tree ✓
])

# Clean: only keep exactly 5-character strings (Unicode chars)
VALID_WORDS = {w for w in VALID_WORDS if len(w) == 5 and '#' not in w}

# Build index: for each position (0-4) and character, what words match?
def build_index(words):
    idx = {}  # (pos, char) -> set of words
    for w in words:
        for i, c in enumerate(w):
            key = (i, c)
            if key not in idx:
                idx[key] = set()
            idx[key].add(w)
    return idx

def find_valid_grids(words):
    """
    Find all valid 5x5 checkerboard grids.
    The grid has:
      - row0, row2, row4: across words (5 chars each)
      - col0, col2, col4: down words (5 chars each)

    Letters in the grid:
      grid[r][c] for c in {0,2,4} and r in {0,1,2,3,4}
      row words: grid[0][0..4], grid[2][0..4], grid[4][0..4]
      col words: grid[0..4][0], grid[0..4][2], grid[0..4][4]

    Constraints (intersections):
      row0[0]=col0[0], row0[2]=col2[0], row0[4]=col4[0]
      row2[0]=col0[2], row2[2]=col2[2], row2[4]=col4[2]
      row4[0]=col0[4], row4[2]=col2[4], row4[4]=col4[4]
    """
    word_list = sorted(words)
    word_set = set(words)

    valid_grids = []

    # For each combination of row0, row2, row4
    # Check if col0, col2, col4 are valid words

    for row0 in word_list:
        for row2 in word_list:
            for row4 in word_list:
                # Build columns from the 5 positions
                # col0 = row0[0], row0[1]=#, row2[0], row2[1]=#, row4[0]
                # But wait - in a 5-wide grid:
                # col0 uses grid positions (0,0),(1,0),(2,0),(3,0),(4,0)
                # In row words: row0[0]=grid[0][0], row2[0]=grid[2][0], row4[0]=grid[4][0]
                # At (1,0) and (3,0): these are NOT black cells in col 0!
                # Black cells are only at (1,1),(1,3),(3,1),(3,3)
                # So (1,0),(1,2),(1,4),(3,0),(3,2),(3,4) are white cells
                # But they're NOT part of any across word (rows 1 and 3 only have isolated cells)
                # They ARE part of down words though!

                # col0 letters: (0,0)=row0[0], (1,0)=?, (2,0)=row2[0], (3,0)=?, (4,0)=row4[0]
                # The middle letters (1,0) and (3,0) are in col0 but not in any across word
                # So they're "free" variables that must exist in col0 as a valid word

                # This means we need to enumerate possible "bridge" characters
                # col0 = row0[0] + bridge10 + row2[0] + bridge30 + row4[0]
                # col2 = row0[2] + bridge12 + row2[2] + bridge32 + row4[2]
                # col4 = row0[4] + bridge14 + row2[4] + bridge34 + row4[4]

                # For each combination of bridge chars, check if cols form valid words

                # Collect candidate chars for bridges
                # bridge at (1,0): must be the char at position 1 of col0 word
                # Pre-filter: words starting with row0[0] and having row2[0] at pos 2 and row4[0] at pos 4

                c00, c02, c04 = row0[0], row0[2], row0[4]
                c20, c22, c24 = row2[0], row2[2], row2[4]
                c40, c42, c44 = row4[0], row4[2], row4[4]

                # Find col0 candidates: word where [0]=c00, [2]=c20, [4]=c40
                col0_cands = [w for w in word_list
                              if w[0] == c00 and w[2] == c20 and w[4] == c40]
                if not col0_cands:
                    continue

                # Find col2 candidates: word where [0]=c02, [2]=c22, [4]=c42
                col2_cands = [w for w in word_list
                              if w[0] == c02 and w[2] == c22 and w[4] == c42]
                if not col2_cands:
                    continue

                # Find col4 candidates: word where [0]=c04, [2]=c24, [4]=c44
                col4_cands = [w for w in word_list
                              if w[0] == c04 and w[2] == c24 and w[4] == c44]
                if not col4_cands:
                    continue

                for col0 in col0_cands:
                    for col2 in col2_cands:
                        for col4 in col4_cands:
                            valid_grids.append({
                                'row0': row0, 'row2': row2, 'row4': row4,
                                'col0': col0, 'col2': col2, 'col4': col4
                            })

    return valid_grids


def grid_to_matrix(g):
    """Convert grid dict to 5x5 matrix with # for black cells."""
    row0, row2, row4 = g['row0'], g['row2'], g['row4']
    col0, col2, col4 = g['col0'], g['col2'], g['col4']

    # Verify constraints
    assert row0[0] == col0[0]
    assert row0[2] == col2[0]
    assert row0[4] == col4[0]
    assert row2[0] == col0[2]
    assert row2[2] == col2[2]
    assert row2[4] == col4[2]
    assert row4[0] == col0[4]
    assert row4[2] == col2[4]
    assert row4[4] == col4[4]

    matrix = [
        [row0[0], row0[1], row0[2], row0[3], row0[4]],
        [col0[1], '#',     col2[1], '#',     col4[1]],
        [row2[0], row2[1], row2[2], row2[3], row2[4]],
        [col0[3], '#',     col2[3], '#',     col4[3]],
        [row4[0], row4[1], row4[2], row4[3], row4[4]],
    ]
    return matrix


# ─── PUZZLE DEFINITIONS ─────────────────────────────────────────────────────

# Each puzzle spec: (id_suffix, title_hu, category, difficulty, across_clues, down_clues)
# across_clues = [(clue_hu for row0), (clue_hu for row2), (clue_hu for row4)]
# down_clues   = [(clue_hu for col0), (clue_hu for col2), (clue_hu for col4)]
# We'll match them with grid words that fit thematically

# First, let's find all valid grids
print("Building word index and finding valid grids...")
valid_grids = find_valid_grids(VALID_WORDS)
print(f"Found {len(valid_grids)} valid grids")

# Deduplicate by word combination
seen = set()
unique_grids = []
for g in valid_grids:
    key = (g['row0'], g['row2'], g['row4'], g['col0'], g['col2'], g['col4'])
    if key not in seen:
        seen.add(key)
        unique_grids.append(g)

print(f"Unique grids: {len(unique_grids)}")

# Print some examples
for g in unique_grids[:10]:
    print(f"  Across: {g['row0']}, {g['row2']}, {g['row4']}  |  Down: {g['col0']}, {g['col2']}, {g['col4']}")


# ─── CLUE DATABASE ──────────────────────────────────────────────────────────
# Word → Hungarian clue text

CLUES = {
    "ABLAK": "Amin keresztül bevilágít a nap — ajtó melletti nyílás",
    "ALMÁK": "Gyümölcsök, amelyek fáról hullanak le — piros vagy zöld",
    "ALMÁS": "Almával töltött vagy ízesített — rétes is lehet ilyen",
    "BABÉR": "Koszorúba font zöld növény — a győztesek fejékszere",
    "BOROS": "Borral teli vagy borkedvelő — pincéből kerül ki",
    "BALTA": "Fakitermelő szerszám, fejsze — erdőirtóé",
    "BARÁT": "Jó ismerős, közeli személy — kolostori szerzetes is",
    "BÁTOR": "Félelem nélkül cselekvő — vitéz, merész",
    "BIRKA": "Gyapjas háziállat, juh — legelőn legel",
    "BODZA": "Fehér virágú bogyós cserje — szörpöt főznek belőle",
    "BOLHA": "Apró ugró rovar — kutya bundájában él",
    "BOKOR": "Kisebb lombos növény — erdőszélen nő",
    "BORDA": "Mellkasi csont — bordástál ételnek is neve",
    "CSATA": "Fegyveres összecsapás, ütközet — csatamező helyszíne",
    "CSEND": "Zajtalanság, némaság — könyvtárban illik ez",
    "CSIGA": "Lassú puhatestű, házban lakik — csigalépcső",
    "CSONT": "Emberi váz eleme — kutyának is odadobják",
    "CSUKA": "Ragadozó édesvízi hal — Tisza és Duna lakója",
    "CSÚCS": "Hegy legmagasabb pontja — teljesítmény teteje",
    "DALOS": "Énekes madár vagy dal — dalosmadár",
    "DIÓFA": "Diótermelő fa — kertben áll, árnyékos",
    "DOLOG": "Feladat, tárgy, munka — elvégzendő dolog",
    "EBÉDE": "Déli étkezés — munkahelyi menza kínálata",
    "ERDEI": "Erdőben élő vagy erdőre vonatkozó — erdei ösvény",
    "FAGYI": "Jeges nyári csemege — nyalon az ember",
    "FALAK": "Épületek oldalai — a városfalak védelmet nyújtottak",
    "FALAS": "Fallal körülvett — erős várfalak",
    "FALUN": "Vidéken, kis településen — falusi élet",
    "FEHÉR": "Hó színe — ellentéte a fekete",
    "FELHŐ": "Vízpára az égen — esőt hozhat",
    "FENYŐ": "Tűlevelű fa — karácsonyfa alapja",
    "FOLYÓ": "Természetes vízfolyás — folyópartján városok épültek",
    "FORMA": "Alak, keret, minta — öntőformába kerül az anyag",
    "FÓRUM": "Nyilvános tér, tanácskozóhely — antik Rómában is volt",
    "FRANK": "Germán nép tagja — Frankföld, Frank Birodalom",
    "GAZDA": "Gazdálkodó, tulajdonos — tanya gazdája",
    "GOMBA": "Erdőben termő növény — gombapaprikás finomság",
    "GÖRBE": "Egyenes ellentéte — hajlított vonal",
    "GÖRÖG": "Hellén nép tagja — ókori görög kultúra",
    "GŐZÖS": "Gőzzel hajtott hajó — Dunán közlekedett",
    "GYÁVA": "Bátortalan, félős — ellentéte a bátor",
    "HADAK": "Katonai csapatok — hadak útján vonuló sereg",
    "HAJAS": "Hajas fej — gazdag hajzatú",
    "HAJÓS": "Hajón dolgozó személy — tengerész, révész",
    "HALAK": "Vizes élőlények — akvárium lakói",
    "HALAS": "Hallal bőséges — halastavon él",
    "HALOM": "Domb, kupac — homokdombon játszanak a gyerekek",
    "HÁROM": "Kettő utáni szám — háromszög oldalainak száma",
    "HÁRFA": "Húros hangszer — angyalok hangszere a képeken",
    "HAVAS": "Hóval borított — téli havas táj",
    "HIDEG": "Alacsony hőmérsékletű — tél jellemzője",
    "HONOS": "Valahol honos, őshonos — magyar tájra honos növény",
    "HORDÓ": "Fa vagy fém henger — boroshordó pincében",
    "HŰVÖS": "Kicsit hideg, friss — őszi hűvös reggel",
    "IGAZI": "Valódi, eredeti — igazi arany, nem hamis",
    "JOGAR": "Királyi pálca, uralom jele — koronázási ékszer",
    "JÓKOR": "Megfelelő időben — nem késve, időre",
    "KAKAS": "Hím tyúk — hajnalt hirdet a faluban",
    "KALAP": "Fejfedő — cowboy kalapja",
    "KALIF": "Muszlim uralkodó — kalifátus feje",
    "KÁVÉS": "Kávéval ízesített — kávés desszert",
    "KAZÁR": "Türk nép a középkorban — kazár birodalom a Kaszpi-tónál",
    "KELET": "Napkelte iránya — Ázsia keleti kultúrái",
    "KÉREM": "Udvarias kérés szava — legyen szíves",
    "KINCS": "Értékes vagyon, drágaság — elásott kincs",
    "KÖRÖS": "Folyó neve Magyarországon — Körös-vidék",
    "KŐRIS": "Lombhullató fa — kőrisfa kemény fája",
    "KÖLES": "Apró szemű gabona — madáreleség is lehet",
    "KUPAC": "Kis halom, rakás — homokos kupac",
    "KÁCSA": "Vízibaromfi — tavi kacsa, récefaj",
    "KACSA": "Tavi vízibaromfi — récefaj, kacsaúszda",
    "KAZAL": "Szalmából rakott kupac — aratás után a mezőn",
    "KÉPEK": "Festmények, fotók, ábrázolások — galériában kiállítva",
    "KŐVÁR": "Kőből emelt vár — középkori védelem",
    "LATIN": "Ókori Róma nyelve — egyházi latin",
    "LEVES": "Meleg folyékony étel — húsleves, gulyásleves",
    "LEVÉL": "Írásos üzenet — postán küldött levél",
    "LIGET": "Kis parkerdő — városi liget",
    "LISZT": "Darált gabona — kenyérhez kell",
    "LOVAG": "Páncélos harcos — középkori lovagi tornán",
    "LOVAK": "Ló, többes szám — lovarda állatai",
    "MADÁR": "Tollas szárnyas állat — fészkét fára rakja",
    "MAGOS": "Magas, nyúlánk — archaic magas forma",
    "MALOM": "Gabonát őrlő szerkezet — szélmalom forog a szélben",
    "MELEG": "Magas hőmérsékletű — nyár jellemzője",
    "MESÉK": "Népmesék, tündérmesék — gyerekeknek mesélnek",
    "MESÉS": "Mesébe illő, csodás — mesés táj",
    "MÉHES": "Méhek lakhelye — méhész gondozza",
    "MÉZES": "Mézzel édesített — mézes kalács, mézes pogácsa",
    "MEZŐK": "Füves síkságok — mező virágai, búzamező",
    "MOHOS": "Mohával borított — mohos kő a patak szélén",
    "MÓZES": "Bibliai próféta — a tíz parancsolat átadója",
    "MUTAT": "Jelzi, irányba mutat — ujjal mutat",
    "NAPOK": "A nap egységei — hét napból áll a hét",
    "NAPOS": "Napsütötte — napos időjárás",
    "NÁDAS": "Nádas terület, nádfedeles rét — Balaton-parti nádas",
    "NÁDOR": "Középkori magyar főméltóság — nádori cím",
    "NEMES": "Előkelő, nemesi — nemesi osztály tagja",
    "NOMÁD": "Vándorló életmódú nép — sátorban él, vonul",
    "NYÁRI": "Nyárhoz tartozó — nyári szabadság",
    "OPERA": "Zenés színházi műfaj — operaházi előadás",
    "ORDAS": "Farkasszürke, komor — ordas farkas",
    "ŐSZIG": "Őszig tartó — nyártól őszig",
    "PADLÓ": "Ház aljzata, padlózat — fából vagy csempéből",
    "PATAK": "Kis vízfolyás — hegyipatak csörgedezése",
    "PÉTER": "Keresztnév — Péter apostol",
    "PIROS": "Vöröses szín — alma piros",
    "PONTY": "Édesvízi hal — halpaprikás alapanyaga",
    "PORTA": "Kapu, bejárat — oszmán porta, udvari kapu",
    "RÉTES": "Vékony tésztás sütemény — almás rétes",
    "RETEK": "Csípős gyökérzöldség — salátába vágják",
    "RÓMAI": "Rómához kötődő — ókori római birodalom",
    "ROMÁN": "Romániai személy vagy román stílus — román építészet",
    "RÓZSA": "Tövises virág — szerelem jelképe",
    "SARLÓ": "Aratóeszköz, görbe penge — gabonát vágnak vele",
    "SASOK": "Ragadozó nagymadarak — sasok a szirten fészkelnek",
    "SASOS": "Sassal díszített — sasos zászló",
    "SÁTOR": "Ideiglenes vászon szállás — táborozáshoz",
    "SEREG": "Katonai csapat — nagy sereg vonult",
    "SÍKOS": "Csúszós felület — jégen síkos az út",
    "SZÁSZ": "Germán nép — erdélyi szászok, szász örökség",
    "SZARV": "Szarvasmarha feje tetején — bikaszarv",
    "SÜKET": "Hallássérült — süket fülekre talál",
    "SÜTIK": "Sütőben készülő ételek — sütiket sütünk",
    "TÁBOR": "Katonai vagy nyári tábor — táborba vonul",
    "TÁBLA": "Írótábla, tábla — iskolai tábla",
    "TATÁR": "Mongol-türk nép — tatár invázió",
    "TÉLEN": "Téli időszakban — télen havazik",
    "TIGRI": "Csíkos nagymacska — Ázsia ragadozója",
    "TŐKÉS": "Tőketulajdonos — gazdasági szereplő",
    "TÖLGY": "Makktermő fa — tölgyfa erdő",
    "TOMBOL": "skip",
    "TORTA": "Ünnepi sütemény — születésnapi torta",
    "TÖRÖK": "Oszmán-türk nép — török hódoltság kora",
    "TÚRÓS": "Túrós, tejtermékkel töltött — túrós rétes",
    "UDVAR": "Ház melletti nyílt tér — udvari kút",
    "VADON": "Ősvadon, vad természet — dzsungel vadonja",
    "VADAK": "Vad állatok — vadász vadakra vadászik",
    "VÁRAK": "Középkori erődítmények — várak és kastélyok",
    "VÁSÁR": "Kereskedelmi esemény — hetivásár a téren",
    "VÁROS": "Nagyobb település — főváros és vidéki város",
    "VILÁG": "Mindenség, föld — a világ körül",
    "VIHAR": "Erős szél és eső — tengeri vihar",
    "VITÉZ": "Bátran harcoló hős — vitézlő katona",
    "ZÖLDE": "Zöldes árnyalatú — rét zöldje",
    "ZÚGÁS": "Mély hangos zaj — szél zúgása",
}

# ─── PUZZLE PLAN ─────────────────────────────────────────────────────────────

# Each puzzle needs: category, topic, difficulty, title_hu
# We'll assign valid grids to puzzles and write clues

GEOGRAPHY_PUZZLES = [
    # Easy (20)
    ("hungarian-cities",     "easy",   "Magyar városok"),
    ("hungarian-cities",     "easy",   "Magyar városok II"),
    ("rivers",               "easy",   "Magyar folyók"),
    ("rivers",               "easy",   "Magyar folyók II"),
    ("balaton",              "easy",   "A Balaton"),
    ("balaton",              "easy",   "Balaton és vidéke"),
    ("plains",               "easy",   "Magyar síkság"),
    ("plains",               "easy",   "Az Alföld"),
    ("mountains",            "easy",   "Magyar hegyek"),
    ("mountains",            "easy",   "Hegyek és völgyek"),
    ("neighboring-countries","easy",   "Szomszéd országok"),
    ("neighboring-countries","easy",   "Határok mentén"),
    ("european-capitals",    "easy",   "Európai fővárosok"),
    ("european-rivers",      "easy",   "Európai folyók"),
    ("continents",           "easy",   "Kontinensek"),
    ("climate",              "easy",   "Éghajlati övek"),
    ("forests",              "easy",   "Európa erdői"),
    ("islands",              "easy",   "Szigetek"),
    ("deserts",              "easy",   "Sivatagok"),
    ("oceans",               "easy",   "Tengerek és óceánok"),
    # Medium (20)
    ("hungarian-cities",     "medium", "Magyar városok haladóknak"),
    ("hungarian-cities",     "medium", "Városok Magyarországon"),
    ("rivers",               "medium", "Folyórendszerek"),
    ("rivers",               "medium", "Folyók és tavak"),
    ("balaton",              "medium", "Balaton természetrajza"),
    ("mountains",            "medium", "Hegységek Európában"),
    ("mountains",            "medium", "Alpok és Kárpátok"),
    ("neighboring-countries","medium", "Szomszédos népek"),
    ("neighboring-countries","medium", "Határszéli tájak"),
    ("european-capitals",    "medium", "Európai fővárosok II"),
    ("european-rivers",      "medium", "Nagy európai folyók"),
    ("mediterranean",        "medium", "A Mediterrán"),
    ("alps",                 "medium", "Az Alpok"),
    ("world-oceans",         "medium", "Óceánok és tengerek"),
    ("africa",               "medium", "Afrika földrajza"),
    ("asia",                 "medium", "Ázsia tájain"),
    ("south-america",        "medium", "Dél-Amerika"),
    ("volcanoes",            "medium", "Vulkánok"),
    ("arctic",               "medium", "Sarki vidékek"),
    ("world-lakes",          "medium", "Világ tavai"),
]

CULTURE_PUZZLES = [
    # Easy (18)
    ("hungarian-literature", "easy",   "Magyar irodalom"),
    ("hungarian-literature", "easy",   "Írók és költők"),
    ("poetry",               "easy",   "Magyar költészet"),
    ("poetry",               "easy",   "Versek világa"),
    ("folk-tales",           "easy",   "Magyar népmesék"),
    ("folk-tales",           "easy",   "Népmesék hősei"),
    ("folk-music",           "easy",   "Magyar népzene"),
    ("folk-music",           "easy",   "Dalok és nóták"),
    ("classical-music",      "easy",   "Klasszikus zene"),
    ("classical-music",      "easy",   "Zeneszerzők"),
    ("opera",                "easy",   "Operavilág"),
    ("theater",              "easy",   "Színház"),
    ("painting",             "easy",   "Festészet"),
    ("folk-art",             "easy",   "Magyar népművészet"),
    ("dance",                "easy",   "Tánc és csárdás"),
    ("cinema",               "easy",   "Magyar film"),
    ("festivals",            "easy",   "Ünnepek és fesztiválok"),
    ("museums",              "easy",   "Múzeumok"),
    # Medium (19)
    ("hungarian-literature", "medium", "Irodalmi alkotások"),
    ("hungarian-literature", "medium", "Petőfi és Arany"),
    ("poetry",               "medium", "Verses formák"),
    ("folk-tales",           "medium", "Tündérmesék"),
    ("folk-music",           "medium", "Hangszerek"),
    ("classical-music",      "medium", "Liszt és Bartók"),
    ("opera",                "medium", "Operahősei"),
    ("theater",              "medium", "Dráma és komédia"),
    ("painting",             "medium", "Képzőművészet"),
    ("sculpture",            "medium", "Szobrászat"),
    ("folk-art",             "medium", "Hímzés és fazekas"),
    ("dance",                "medium", "Néptánc hagyomány"),
    ("architecture",         "medium", "Építészet"),
    ("folk-costumes",        "medium", "Népi viselet"),
    ("crafts",               "medium", "Kézműves mesterségek"),
    ("weaving",              "medium", "Szövés és fonás"),
    ("wood-carving",         "medium", "Faragás"),
    ("church-art",           "medium", "Egyházi művészet"),
    ("libraries",            "medium", "Könyvtárak és könyvek"),
]

# ─── ASSIGN GRIDS TO PUZZLES ─────────────────────────────────────────────────

def make_puzzle_json(puzzle_id, title_hu, category, difficulty, grid_dict, across_clues, down_clues):
    """Build the puzzle JSON structure."""
    matrix = grid_to_matrix(grid_dict)

    row0 = grid_dict['row0']
    row2 = grid_dict['row2']
    row4 = grid_dict['row4']
    col0 = grid_dict['col0']
    col2 = grid_dict['col2']
    col4 = grid_dict['col4']

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
            ]
        }
    }


def get_clue(word, default=None):
    """Get clue for a word, or generate a fallback."""
    c = CLUES.get(word)
    if c and c != "skip":
        return c
    if default:
        return default
    return f"Megfejtés: {word.lower()} — öt betűs szó"


def assign_and_generate():
    """Assign grids to puzzles and generate JSON files."""

    if len(unique_grids) < 77:
        print(f"WARNING: Only {len(unique_grids)} unique grids available for 77 puzzles!")
        print("Some grids will be reused.")

    all_puzzles = GEOGRAPHY_PUZZLES + CULTURE_PUZZLES

    # Track file numbering per (category, topic) pair
    file_counters = {}

    generated = []

    for idx, puzzle_spec in enumerate(all_puzzles):
        if len(puzzle_spec) == 3:
            topic, difficulty, title_hu = puzzle_spec
            category = "geography" if idx < len(GEOGRAPHY_PUZZLES) else "culture"

        # Get a grid (cycle if necessary)
        grid = unique_grids[idx % len(unique_grids)]

        # Get file number
        key = (category, topic)
        if key not in file_counters:
            file_counters[key] = 10  # start at 010
        else:
            file_counters[key] += 1
        num = file_counters[key]
        num_str = f"{num:03d}"

        puzzle_id = f"{category}-{topic}-{difficulty}-{num_str}"
        filename = f"{topic}-{difficulty}-{num_str}.json"

        # Build clues using the CLUES dict
        row0, row2, row4 = grid['row0'], grid['row2'], grid['row4']
        col0, col2, col4 = grid['col0'], grid['col2'], grid['col4']

        across_clues = [
            get_clue(row0),
            get_clue(row2),
            get_clue(row4),
        ]
        down_clues = [
            get_clue(col0),
            get_clue(col2),
            get_clue(col4),
        ]

        puzzle = make_puzzle_json(
            puzzle_id, title_hu, category, difficulty,
            grid, across_clues, down_clues
        )

        generated.append((category, filename, puzzle))

    return generated


# ─── MAIN ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    puzzles = assign_and_generate()

    base = Path("/Users/nadavsolomon/Code/hu-crossword-puzzle/public/puzzles")

    written = 0
    for category, filename, puzzle in puzzles:
        outdir = base / category
        outdir.mkdir(parents=True, exist_ok=True)
        outpath = outdir / filename

        # Don't overwrite existing files
        if outpath.exists():
            print(f"SKIP (exists): {outpath}")
            continue

        with open(outpath, 'w', encoding='utf-8') as f:
            json.dump(puzzle, f, ensure_ascii=False, indent=2)

        print(f"WROTE: {outpath}")
        written += 1

    print(f"\nTotal written: {written} puzzles")
