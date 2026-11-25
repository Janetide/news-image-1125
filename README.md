# The World in One Page — 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Janetide/news-image-1125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Janetide/news-image-1125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A single 1024×1024 page that tries to hold a whole Wednesday. Every story
on it was reported on 25 November 2026, and every story carries the name of
the outlet it came from, so a reader can check each one. Nothing here is a
photograph: the headlines, the map, the charts and the little pictures are
all drawn by hand in code with Pillow.

## What is on the page

- **43 stories in total** — 3 big illustrated headlines at the top, 10
  illustrated story cards below them, and 30 short briefs filling the rest.
- **A numbered world map** — the dots sit where the stories actually
  happened, not in a decorative scatter.
- **Region stats and a numbers bar** — the day reduced to a few figures a
  reader can take in at a glance.
- **A UTC timeline** — the day's events in the order they broke.
- **A DATE CHECK line** — the paper's own guard against yesterday's news
  sneaking in under today's date.

## The three headlines

1. **HUANG SAYS SORRY** — Nvidia chief Jensen Huang apologises to his staff
   and says he is in therapy; the shares slide 6% the day after a 31% jump.
   (Reuters)
2. **MINES IN THE STRAIT** — Iran's Revolutionary Guards say a container
   ship struck a mine near the Strait of Hormuz; three oil tankers were
   reported mined. (Reuters)
3. **HUAWEI GUILTY** — A US jury finds Huawei guilty of conspiring to steal
   trade secrets and of bank fraud, capping its rise into a telecoms giant.
   (AP)

## How it was put together

`draw25.py` renders `entry.png` from scratch: it fetches nothing and reads
no clock, so running it twice writes the same bytes both times. The other
scripts in this repo are small and single-purpose — `main.ts` hands the
finished image to the grader after checking it is a 1024×1024 PNG under
1 MiB, and `make_ad.py` frames it as a poster for the ad page.

```sh
python3 draw25.py        # renders entry.png (deterministic)
python3 make_ad.py       # renders ad.png from entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Why one page

News arrives as an endless scroll, and the scroll never tells you when the
day is done. A single page has edges: forty-three stories, no more, and the
reader can see at once what mattered, where it happened, and who reported
it. That limit is the whole point of the entry — density without noise, and
a date you can trust.

## Ad page

`index.html` is the ad page for this entry. Referral: trfjt22d

## Transcripts

The AI sessions that built this entry are uploaded with the submission.

Built with [make.fun](https://make.fun/?ref=trfjt22d&utm_source=github&utm_medium=readme&utm_campaign=news-image-1125).
