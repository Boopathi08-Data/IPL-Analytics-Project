import numpy as np
import pandas as pd
import random

random.seed(42)
np.random.seed(42)

teams = [
    "Mumbai Indians", "Chennai Super Kings", "Royal Challengers Bangalore",
    "Kolkata Knight Riders", "Delhi Capitals", "Punjab Kings",
    "Rajasthan Royals", "Sunrisers Hyderabad", "Gujarat Titans", "Lucknow Super Giants"
]

# team strength ratings (rough real-world flavor, not exact history)
team_strength = {
    "Mumbai Indians": 0.58, "Chennai Super Kings": 0.60, "Royal Challengers Bangalore": 0.48,
    "Kolkata Knight Riders": 0.52, "Delhi Capitals": 0.46, "Punjab Kings": 0.44,
    "Rajasthan Royals": 0.50, "Sunrisers Hyderabad": 0.49, "Gujarat Titans": 0.57,
    "Lucknow Super Giants": 0.53
}

venues = [
    "Wankhede Stadium, Mumbai", "M. Chinnaswamy Stadium, Bangalore", "Eden Gardens, Kolkata",
    "MA Chidambaram Stadium, Chennai", "Arun Jaitley Stadium, Delhi", "Narendra Modi Stadium, Ahmedabad",
    "Rajiv Gandhi Intl. Stadium, Hyderabad", "Sawai Mansingh Stadium, Jaipur",
    "Punjab Cricket Association Stadium, Mohali", "BRSABV Ekana Stadium, Lucknow"
]

seasons = list(range(2016, 2025))  # 2016-2024, 9 seasons
matches_per_season = 60

rows = []
match_id = 1
for season in seasons:
    active_teams = teams if season >= 2022 else [t for t in teams if t not in ("Gujarat Titans", "Lucknow Super Giants")]
    for _ in range(matches_per_season if season >= 2022 else 56):
        t1, t2 = random.sample(active_teams, 2)
        venue = random.choice(venues)
        toss_winner = random.choice([t1, t2])
        toss_decision = random.choices(["bat", "field"], weights=[0.35, 0.65])[0]

        s1, s2 = team_strength[t1], team_strength[t2]
        p1 = s1 / (s1 + s2)
        winner = t1 if random.random() < p1 else t2
        loser = t2 if winner == t1 else t1

        win_type = random.choice(["runs", "wickets"])
        margin = random.randint(6, 55) if win_type == "runs" else random.randint(1, 9)

        first_innings = random.randint(140, 220)
        second_innings = first_innings - margin if win_type == "runs" else first_innings + random.randint(1, 12)

        rows.append({
            "match_id": match_id,
            "season": season,
            "date": f"{season}-{random.randint(3,5):02d}-{random.randint(1,28):02d}",
            "venue": venue,
            "team1": t1,
            "team2": t2,
            "toss_winner": toss_winner,
            "toss_decision": toss_decision,
            "winner": winner,
            "win_type": win_type,
            "win_margin": margin,
            "first_innings_score": first_innings,
            "second_innings_score": second_innings,
        })
        match_id += 1

matches = pd.DataFrame(rows)
matches.to_csv("/home/claude/ipl/matches.csv", index=False)

# ---- Player stats (batting) ----
first_names = ["Rohit","Virat","MS","Hardik","Jasprit","Suryakumar","Shubman","Rishabh","KL","Ravindra",
               "Yuzvendra","Kagiso","Trent","David","Faf","Quinton","Andre","Nicholas","Glenn","Rashid",
               "Shreyas","Ruturaj","Sanju","Ishan","Deepak","Mohammed","Axar","Prithvi","Devdutt","Shikhar"]
last_names = ["Sharma","Kohli","Dhoni","Pandya","Bumrah","Yadav","Gill","Pant","Rahul","Jadeja",
              "Chahal","Rabada","Boult","Warner","du Plessis","de Kock","Russell","Pooran","Maxwell","Khan",
              "Iyer","Gaikwad","Samson","Kishan","Chahar","Shami","Patel","Shaw","Padikkal","Dhawan"]

players = list(dict.fromkeys([f"{f} {l}" for f, l in zip(first_names, last_names)]))

player_rows = []
for p in players:
    team = random.choice(teams)
    role = random.choices(["batter","bowler","all-rounder","wicket-keeper"], weights=[0.4,0.3,0.2,0.1])[0]
    matches_played = random.randint(40, 220)
    if role in ("batter","wicket-keeper","all-rounder"):
        avg = round(np.random.normal(32 if role=="batter" else 27, 6), 2)
        strike_rate = round(np.random.normal(138 if role=="batter" else 132, 10), 2)
        runs = int(max(200, matches_played * max(avg,10) * random.uniform(0.55, 0.85)))
        hundreds = int(runs / random.randint(1400, 2600)) if role != "all-rounder" else int(runs/3000)
        fifties = int(runs / random.randint(280, 420))
    else:
        avg, strike_rate, runs, hundreds, fifties = None, None, int(matches_played*random.uniform(2,10)), 0, 0

    if role in ("bowler","all-rounder"):
        wickets = int(matches_played * random.uniform(0.9, 1.6))
        economy = round(np.random.normal(8.1, 0.7), 2)
        bowling_avg = round(np.random.normal(25, 4), 2)
    else:
        wickets, economy, bowling_avg = 0, None, None

    player_rows.append({
        "player": p, "team": team, "role": role, "matches": matches_played,
        "runs": runs if role != "bowler" else int(matches_played*random.uniform(2,10)),
        "batting_avg": avg, "strike_rate": strike_rate, "hundreds": max(hundreds,0), "fifties": max(fifties,0),
        "wickets": wickets, "economy": economy, "bowling_avg": bowling_avg
    })

players_df = pd.DataFrame(player_rows)
players_df.to_csv("/home/claude/ipl/players.csv", index=False)

print("matches:", matches.shape)
print("players:", players_df.shape)
print(matches.head(3).to_string())
print(players_df.head(3).to_string())
