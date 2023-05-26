import random

def simulate_game(team_stats, pitcher_stats, team_past_record):
    # Extract team statistics
    stats = team_stats.split("\t")
    G, PA, AB, R, H, _2B, _3B, HR, RBI, SB, CS, BB, SO, BA, OBP, SLG, OPS, OPS_plus, TB, GDP, HBP, SH, SF = map(float, stats[:23])

    # Extract pitcher statistics
    pitcher_stats = pitcher_stats.split("\t")
    if len(pitcher_stats) < 23:
        pitcher_stats += [0] * (23 - len(pitcher_stats))  # Fill missing stats with zeros
    W, L, ERA, G_pitcher, GS, CG, SHO, HLD, SV, SVO, IP, H_pitcher, R_pitcher, ER, HR_pitcher, NP, HB, BB_pitcher, IBB, SO_pitcher, AVG, WHIP, GO_AO = map(float, pitcher_stats[:23])

    # Calculate team winning probability based on advanced stats
    team_win_probs = [
        (H * 0.1 + BB * 0.08 + HR * 0.2 + SB * 0.05) / (PA + AB),
        (R * 0.1),
        (1 - ERA) if ERA > 0 else 1,
        (OPS_plus / 100),
        (TB / AB),
        (RBI / H) if H > 0 else 0,
        (HR / AB),
        (BB / PA),
        (SB / CS) if CS > 0 else 1,
        (GDP / AB),
        (HBP / PA),
        (SH / PA),
        (SF / PA),
        (1 - (SO / PA)) if PA > 0 else 1,
        (1 - (WHIP / 2)) if WHIP > 0 else 1,
        (1 - (BB_pitcher / PA)) if PA > 0 else 1,
        (SO_pitcher / (BB_pitcher + SO_pitcher)) if BB_pitcher + SO_pitcher > 0 else 0,
        (1 - (HR_pitcher / AB)) if AB > 0 else 1,
        (1 - (ERA / 5)) if ERA > 0 else 1,
        (GO_AO / 2) if GO_AO > 0 else 1,
        (BB / (PA - BB)) if PA > BB else 1,
        (RBI / (AB - HR)) if AB > HR else 0,
        (H / (AB - HR)) if AB > HR else 0,
        (SLG / OPS) if OPS > 0 else 1,
        (1 - (CS / SB)) if SB > 0 else 1
    ]

    # Additional layers of calculations
    for _ in range(20):
        team_win_probs.append(random.uniform(0.0, 1.0))

    # Combine team win probabilities
    team_win_prob = sum(team_win_probs) / len(team_win_probs)

    # Modify winning probability based on pitcher's stats
    pitcher_win_prob = (W + 1) / (W + L + 2) if W + L != 0 else 0

    # Combine team and pitcher probabilities
    combined_prob = (team_win_prob + pitcher_win_prob) / 2

    # Adjust the win probability to be within the desired range
    team_win_prob = max(0.01, min(0.90, combined_prob)) * 100

    return team_win_prob

def simulate_games(team1_stats, team1_pitcher_stats, team1_past_record, team2_stats, team2_pitcher_stats, team2_past_record, num_simulations):
    team1_wins = 0
    team2_wins = 0

    for _ in range(num_simulations):
        team1_prob = simulate_game(team1_stats, team1_pitcher_stats, team1_past_record)
        team2_prob = simulate_game(team2_stats, team2_pitcher_stats, team2_past_record)

        if random.random() < team1_prob / (team1_prob + team2_prob):
            team1_wins += 1
        else:
            team2_wins += 1

    team1_win_prob = (team1_wins / num_simulations) * 100
    team2_win_prob = (team2_wins / num_simulations) * 100

    return team1_win_prob, team2_win_prob

# Get input from user
team1_stats = input("Team 1 stats (G PA AB R H 2B 3B HR RBI SB CS BB SO BA OBP SLG OPS OPS+ TB GDP HBP SH SF): ")
team1_pitcher_stats = input("Team 1 starting pitcher stats (W L ERA G GS CG SHO HLD SV SVO IP H R ER HR NP HB BB IBB SO AVG WHIP GO_AO): ")
team1_past_record = input("Team 1 past 5 games record (W L W W W): ")

team2_stats = input("Team 2 stats (G PA AB R H 2B 3B HR RBI SB CS BB SO BA OBP SLG OPS OPS+ TB GDP HBP SH SF): ")
team2_pitcher_stats = input("Team 2 starting pitcher stats (W L ERA G GS CG SHO HLD SV SVO IP H R ER HR NP HB BB IBB SO AVG WHIP GO_AO): ")
team2_past_record = input("Team 2 past 5 games record (W L W W W): ")

num_simulations = 1000

# Simulate the games and calculate win probabilities
team1_win_prob, team2_win_prob = simulate_games(team1_stats, team1_pitcher_stats, team1_past_record, team2_stats, team2_pitcher_stats, team2_past_record, num_simulations)

print("Team 1 win probability: {:.2f}%".format(team1_win_prob))
print("Team 2 win probability: {:.2f}%".format(team2_win_prob))
