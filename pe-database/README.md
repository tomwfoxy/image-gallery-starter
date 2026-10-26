# UK Lower-Mid-Market PE Database

A growing list of UK-based lower-mid-market private equity firms and their portfolio companies.

| File | What it is |
|---|---|
| `firms.json` | The source of truth. Edit this file only. |
| `DATABASE.md` | Readable version, generated from `firms.json` |
| `portfolio.csv` | One row per portfolio company, for Excel. Generated. |
| `candidates.md` | Queue of firms still to research, plus rejected firms |
| `news/YYYY-MM-DD.md` | Weekly news scans: deals, exits and other changes |
| `render.py` | Rebuilds `DATABASE.md` and `portfolio.csv`: `python3 pe-database/render.py` |

## Automation

- **Weekdays:** research the next 10 firms from `candidates.md`, add them and their portfolios to
  `firms.json`, then run `render.py`, commit and push.
- **Sunday:** search the news for every firm in the database (new investments, exits, bolt-ons,
  fund closes, team changes). Write `news/<date>.md` and update `firms.json`, including
  moving sold companies to `exited`.
- **Monday morning:** email the latest weekly scan to the owner.

## Data quality

Portfolio entries marked `unverified` come from third-party aggregators (PitchBook, CB Insights, Caplight,
adviser deal notes) and haven't been confirmed against the firm's own website. Firm websites can't be
reached from the automation environment, so they are checked through search results instead. The
weekly scan upgrades entries to `active` or `exited` when news confirms them.
