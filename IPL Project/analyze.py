import pandas as pd
import json

matches = pd.read_csv("/home/claude/ipl/matches.csv")
players = pd.read_csv("/home/claude/ipl/players.csv")

summary = {}

# Total wins by team
wins = matches['winner'].value_counts().to_dict()
summary['wins_by_team'] = wins

# Matches played by team
played = pd.concat([matches['team1'], matches['team2']]).value_counts().to_dict()
summary['matches_played_by_team'] = played

# Win % by team
win_pct = {t: round(wins.get(t,0)/played[t]*100,1) for t in played}
summary['win_pct_by_team'] = dict(sorted(win_pct.items(), key=lambda x:-x[1]))

# Toss impact: how often toss winner also won match
matches['toss_win_match_win'] = matches['toss_winner'] == matches['winner']
toss_impact = round(matches['toss_win_match_win'].mean()*100,1)
summary['toss_win_match_win_pct'] = toss_impact

# Toss decision split
summary['toss_decision_split'] = matches['toss_decision'].value_counts().to_dict()

# Season-wise avg first innings score (run inflation trend)
season_scores = matches.groupby('season')['first_innings_score'].mean().round(1).to_dict()
summary['season_avg_first_innings'] = season_scores

# Matches per season
season_matches = matches.groupby('season').size().to_dict()
summary['matches_per_season'] = season_matches

# Venue win totals (most matches hosted)
venue_counts = matches['venue'].value_counts().to_dict()
summary['matches_by_venue'] = venue_counts

# Top run scorers
top_batters = players.sort_values('runs', ascending=False).head(8)[['player','team','runs','batting_avg','strike_rate']].to_dict('records')
summary['top_run_scorers'] = top_batters

# Top wicket takers
top_bowlers = players[players['wickets']>0].sort_values('wickets', ascending=False).head(8)[['player','team','wickets','economy','bowling_avg']].to_dict('records')
summary['top_wicket_takers'] = top_bowlers

# Best strike rate (min 1000 runs)
best_sr = players[players['runs']>1500].sort_values('strike_rate', ascending=False).head(6)[['player','team','strike_rate','runs']].to_dict('records')
summary['best_strike_rates'] = best_sr

# Best economy (min 50 wickets)
best_econ = players[players['wickets']>50].sort_values('economy').head(6)[['player','team','economy','wickets']].to_dict('records')
summary['best_economy'] = best_econ

# Win margin averages by win type
summary['avg_win_margin_runs'] = round(matches[matches.win_type=='runs']['win_margin'].mean(),1)
summary['avg_win_margin_wickets'] = round(matches[matches.win_type=='wickets']['win_margin'].mean(),1)

summary['total_matches'] = int(len(matches))
summary['total_seasons'] = int(matches['season'].nunique())
summary['total_players'] = int(len(players))

with open("/home/claude/ipl/summary.json","w") as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2)[:3000])
