# IPL Data Analytics Project

## Contents
- `matches.csv` — 516 match records (2016-2024): teams, venue, toss, result, scores
- `players.csv` — 30 player records: batting & bowling stats
- `generate_data.py` — script that generated the synthetic dataset (swap in real data here)
- `analyze.py` — computes all analytics (win %, toss impact, season trends, top players)
- `summary.json` — output of analyze.py, the computed insights

## Note on the data
This dataset is **synthetically generated** to look realistic (not actual IPL history).
To run on real data, replace matches.csv / players.csv with an actual IPL dataset
(e.g. from Kaggle) using the same column structure, then rerun analyze.py.

## How to run
```
pip install pandas numpy
python3 generate_data.py   # regenerate data (optional)
python3 analyze.py         # recompute summary.json
```

## Key findings
- CSK leads win rate at 67.5%; KKR trails at 39.6%
- Toss winner wins the match only 50.2% of the time — toss has little bearing on outcome
- Teams elect to field first ~65% of the time
- Average first-innings score has stayed flat (176-184 runs) across seasons — no major scoring inflation
- KL Rahul tops the run charts (4,669 runs); David Warner leads wickets (317)
