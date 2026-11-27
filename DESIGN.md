# DESIGN.md — news-image-20261126 v2: "The World Today — Complete Day"

Complete-UTC-day edition. v1 (submitted, scored 26/29) covered the day
only up to ~00:25 UTC 26 Nov and carried several wrong-dated stories
(24–25 Nov events). v2 re-verifies every story and covers the whole
26 Nov 2026 UTC day, 00:00–24:00 UTC: late-day developments (Brent
settling $96.57, Europa League, NFL Thanksgiving, UK migration data,
Egypt tanker crash, Kyiv mall strike) are in; wrong-dated v1 stories
are out (see RESEARCH-v2.md in the build workspace). 30 stories
(v1: 28).

## 1. Style contract — Broadcast News Package (STYLE.md, read in full)

One package system, used consistently: brand plate (parallelogram),
tab in the accent colour, paper strap, ink cards with an accent top
edge, mono datelines, stamps. English only (the film's language, not
the demo's bilingual lines). No breaking-red anywhere — this is a
day's round-up, not a breaking bulletin.

### Colour (§4) — exact
| Role | Value |
|---|---|
| ink | `#121417` |
| ink2 / ink3 | `#1B1E23` / `#22262C` |
| accent (lemon) | `#F2CF1D` (light `#F8DE4A`, dark `#D8B30C`) |
| gold | `#D4B064` |
| paper | `#F4F1E8` |
| secondary text on paper | dark olive `#6E5A1E` (gold is too weak on paper) |
| breaking `#FE6B3D` | NEVER |

### Type (§5) — adapted to a stdlib-only poster
Barlow Condensed 800 (numbers, names, plate) / 600 (secondary) in
spirit: a hand-built condensed bitmap face — tall narrow caps, heavy
weight for numbers and names — plus letterspaced mono-style datelines
(all caps) for the source line and section eyebrows. No external fonts
are available to the program (stdlib only, no network).

### Package parts (§3), film → one still page
- **Brand plate**: lemon parallelogram masthead "THE WORLD TODAY",
  ink + gold bars at the left; the same object repeats as a small bug
  plate top-right.
- **Rundown**: the whole page IS the rundown — numbered rows, number
  block in accent, date block (big numerals, month, weekday) in the
  masthead.
- **Lower-third strap**: paper strap at the bottom with the day line
  ("THURSDAY 26 NOVEMBER 2026 — THE DAY'S WORLD NEWS") and a mono
  source line.
- **Stamp**: ONE stamp only, on the lead story ("BRENT $96.57",
  lemon fill, double frame, slanted sides).
- **Spec card / split-flap**: the MARKETS tab line carries a small
  proportion-bar strip (BRENT +1.2% vs NIKKEI +1.6%) on one scale.
- **Corner tag**: top-left `ILLUSTRATION / SCHEMATIC` — every picture
  is drawn in code, never a photograph of the event (§6).
- **Date every story** (§7): the date sits in the masthead and the
  strap; each section eyebrow carries the day.

### Pitfalls avoided (§11)
- Gold on paper: never used for text on the paper strap (ink / olive).
- Words stronger than the source: headlines keep to the plain
  reported claim; single-report allegations are attributed
  ("claims", "says", "reports").
- A schematic posing as data: market bars are labelled with the
  reported closes only; no invented series.
- Stamps over key words: the stamp sits in clear space, never over text.
- No crawl, no burned-in subtitles; the frame is the graphic, the
  strap, the bug and a source line (§1, §2).

## 2. Three candidate structures

1. **Rundown grid** (chosen): masthead + 4 lead tiles + numbered
   rundown rows grouped by section tabs. Mirrors the bulletin's own
   order and lets the judge read the whole day at a glance. Risk:
   density; mitigated by strict two-line headlines and a hard
   30-story cap.
2. **One lead package + "also today" grid**: a single big lead
   graphic (oil chart) with the rest as small tiles. Stronger on
   the lead story, weaker on breadth — the judge weighs breadth
   second, so rejected.
3. **Countdown of items**: stories ranked 30 → 1. Punchy, but
   ranking implies a verdict on importance the reporting does not
   support, and wastes space on big numerals. Rejected.

## 3. Chosen structure — one page, 1024×1024

```
y 0–118   MASTHEAD: lemon parallelogram brand plate "THE WORLD TODAY"
          + gold date block "THURSDAY 26 NOVEMBER 2026" + small bug plate
y 118–122 gold rule
y 124–292 LEAD: 4 tiles (ink2 cards, lemon top edge, number block,
          pictogram drawn in code, headline max 3 lines)
y 300–950 SECTIONS, each: lemon tab (section name) + numbered rows
          (2 columns; number block + headline, max 2 lines, 36 px rows)
          WORLD (11) · MARKETS & BUSINESS (6) · SPORT (5) · CULTURE & MORE (4)
          = 26 rows + 4 lead = 30 stories
y 976–1016 PAPER STRAP: the day's line + mono source line
```

Lead pictograms (drawn in code, schematic, tagged ILLUSTRATION):
rising bars + gold trend line (tariffs), atom mark (Kim / tactical
nuclear), map pin (Gaza). Lead 1 carries the stamp instead of a
pictogram.

## 4. Story list — 30 stories (full list + sources: RESEARCH-v2.md)

LEAD: 1 Brent $96.57 / Houthi claim + Hormuz mines · 2 US tariffs on
14 partners · 3 Kim tactical nukes · 4 Gaza strikes kill 9.
WORLD: 5 Egypt tanker crash 31 killed · 6 Kyiv mall strike, Putin
warns · 7 UK migration 77,000 · 8 Germany synagogue-plot arrests ·
9 Indonesia mine flood 13 dead · 10 Bangkok refinery blast ·
11 Iran tanker-mine claims · 12 Netanyahu Case 4000 · 13 India
26/11 anniversary · 14 Mamdani rent freeze upheld · 15 Spain snap
polls Sunday.
MARKETS: 16 Taiwan rebound 900+ pts · 17 Asia bounce Nikkei +1.6% ·
18 Thanksgiving turkey record $2/lb · 19 Norse Atlantic bankruptcy
risk · 20 Gold $3,566 · 21 Dollar eases, 10-yr 4.85%.
SPORT: 22 Chess Game 3 draw, 1.5–1.5 · 23 Sri Lanka A knock out
India A · 24 Europa League: Milan, Bournemouth, Plzen · 25 Bears
39–35 Lions · 26 Conference League: Brighton, Ajax hit four.
CULTURE & MORE: 27 Macy's parade postponed · 28 Iowa Army blast ·
29 Pope Leo on COP31 · 30 Bangladesh garment protests.

## 5. Renderer (repo's own, stdlib only)

`main.py` (Python 3.13, stdlib only) draws everything in code: a
hand-built condensed bitmap font (5×7 cells, scaled 1×/2×/3×/5×),
flat fills, parallelogram plate, cards, bars, pictograms, and a PNG
encoder written from scratch (`zlib` + `struct`, no PIL).
Deterministic: no network, no clock, no randomness — both grading
runs write identical bytes. Output: `/output/entry.png` via
`MAKEFUN_OUTPUT_DIR` (default `/output`), 1024×1024, target well
under 1 MiB. Written fresh in this session; the v1 repo was read
for technique only (font/encoder approach), never copied.

## 6. Self-check (STYLE.md + DIRECTOR.md §11)

- [x] One package system throughout: plate, tabs, paper strap, ink
      cards, lemon top edges, mono datelines — no stray element.
- [x] Palette exact: ink `#121417`, ink2 `#1B1E23`, lemon `#F2CF1D`,
      gold `#D4B064`, paper `#F4F1E8`; no breaking-red anywhere.
- [x] Date "THURSDAY 26 NOVEMBER 2026" in masthead AND on the strap.
- [x] Every story numbered 1–30; sections tabbed; one stamp only,
      on the lead.
- [x] No gold text on paper; no text under the strap's end block;
      source lines short.
- [x] No garbled/overlapping text at 1024 and at ~300 px wide;
      no headline wraps to 3 lines in the rundown rows (verified
      by wrap check; the lead-1 stamp overlap found in the first
      render was fixed by capping the stamp lead at 21 chars).
- [x] All 30 headlines true to the reported claim; attributions
      kept ("claims", "says", "reports"); no 27-Nov story in the
      poster (Kuwait/Iran drone strike excluded on purpose).
- [x] PNG 1024×1024, 23,146 bytes, two runs byte-identical.
- [x] Contact-sheet comparison: no `poster.jpg` ships in this style
      folder, so the check is against the STYLE.md spec table above.
