[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/yandreload/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/yandreload/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

# The World in One Day — Tuesday 24 November 2026

Entry for the make.fun bounty
[Sum up 24 November's world news in one image](https://make.fun/bounty/news-image-20261124)
($100 USDC, 50 paid places, closes Thu 26 Nov 2026 07:00 WIB).

## The image

A 1024×1024 newspaper front page, "THE WORLD IN ONE DAY", summing up
Tuesday 24 November 2026 in 10 dated stories across 5 regions:

- **Lead — Strait of Hormuz:** three oil tankers hit naval mines; Iran
  vows "all available means" against the US naval blockade.
- **COP31 collapses** in Antalya — no deal, the first failed climate
  summit since Copenhagen 2009 (ended Sun 22 Nov).
- **Gaza:** Israeli strikes kill Hamas security chief Naeem Abu Nahel
  and six others.
- **Ukraine:** Russian strike on Zaporizhzhia kills 2, wounds 40;
  Kyiv says its naval drones sank a Russian corvette off Libya.
- **Also on Tuesday:** Nvidia reinstates Jensen Huang as CEO; US
  sanctions Iran's shadow banking; fighting in Ituri traps Ebola
  responders; South Korea offers $375,000 rewards to catch AI exam
  cheats.
- **The weekend that led here (Sun 22 Nov):** Mercury orbiters arrive
  after an 8-year cruise; Indonesia factory fire kills at least 24.

Sources for every story: see [SOURCES.md](SOURCES.md).

## How it is built

- `generate.py` — local build tool (Pillow + Liberation fonts). Renders
  `entry.png` from the fixed story text. Not the entrypoint.
- `entry.png` — the committed entry image, 1024×1024, under 1 MiB.
- `main.py` — the entrypoint (Python 3.13, stdlib only). It copies
  `entry.png` to `/output/entry.png`, exactly as the brief suggests
  ("the simplest program copies an image the repository holds"). No
  network, no randomness: two runs write identical bytes.

## Run it

```sh
python3 main.py        # writes /output/entry.png
```

## Verify

```sh
python3 main.py && sha256sum /output/entry.png
python3 main.py && sha256sum /output/entry.png   # same hash
python3 -c "from PIL import Image; im = Image.open('/output/entry.png'); print(im.size, im.format)"
```

## License

MIT — see [LICENSE](LICENSE).
