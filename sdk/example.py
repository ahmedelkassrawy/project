"""
Example script demonstrating the usage of the SWCPY SDK
"""
from swcpy import SWCClient, SWCConfig
from datetime import date

def main():
    # Initialize the SDK client
    config = SWCConfig(
        swc_base_url="http://localhost:8000",
        backoff=True,
        backoff_max_time=30
    )
    
    client = SWCClient(config)
    
    # 1. Check API health
    print("=" * 50)
    print("1. Health Check")
    print("=" * 50)
    health = client.get_health_check()
    print(f"API Status: {health}")
    print()
    
    # 2. Get counts
    print("=" * 50)
    print("2. Get Counts")
    print("=" * 50)
    counts = client.get_counts()
    print(f"Total Leagues: {counts.league_count}")
    print(f"Total Teams: {counts.team_count}")
    print(f"Total Players: {counts.player_count}")
    print()
    
    # 3. List players
    print("=" * 50)
    print("3. List Players (First 5)")
    print("=" * 50)
    players = client.list_players(skip=0, limit=5)
    for player in players:
        print(f"  - {player.first_name} {player.last_name} ({player.position})")
    print()
    
    # 4. Get a specific player
    print("=" * 50)
    print("4. Get Specific Player")
    print("=" * 50)
    if players:
        player = client.get_player(players[0].player_id)
        print(f"Player: {player.first_name} {player.last_name}")
        print(f"Position: {player.position}")
        print(f"GSIS ID: {player.gsis_id}")
        print(f"Performances: {len(player.performances)}")
        print()
    
    # 5. List leagues
    print("=" * 50)
    print("5. List Leagues")
    print("=" * 50)
    leagues = client.list_leagues(limit=5)
    for league in leagues:
        print(f"  - {league.league_name} ({league.scoring_type})")
        print(f"    Teams: {len(league.teams)}")
    print()
    
    # 6. List teams
    print("=" * 50)
    print("6. List Teams (First 5)")
    print("=" * 50)
    teams = client.list_teams(limit=5)
    for team in teams:
        print(f"  - {team.team_name} (League ID: {team.league_id})")
        print(f"    Players: {len(team.players)}")
    print()
    
    # 7. List performances
    print("=" * 50)
    print("7. List Performances (First 5)")
    print("=" * 50)
    performances = client.list_performances(limit=5)
    for perf in performances:
        print(f"  - Player {perf.player_id}, Week {perf.week_number}: {perf.fantasy_points} points")
    print()
    
    print("=" * 50)
    print("Example completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    main()
