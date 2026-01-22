# Quick Start Guide

This guide will help you get started with the SWCPY SDK in just a few minutes.

## Prerequisites

- Python 3.10 or higher
- The SWC API running (typically on http://localhost:8000)

## Installation

1. Navigate to the SDK directory:
```bash
cd sdk
```

2. Install the SDK:
```bash
pip install -e .
```

## Your First API Call

Create a new Python file and add the following code:

```python
from swcpy import SWCClient, SWCConfig

# Configure the client
config = SWCConfig(swc_base_url="http://localhost:8000")
client = SWCClient(config)

# Check if the API is running
health = client.get_health_check()
print(health)  # Should print: {'message': 'API health check successful'}

# Get data counts
counts = client.get_counts()
print(f"Total players: {counts.player_count}")
print(f"Total teams: {counts.team_count}")
print(f"Total leagues: {counts.league_count}")
```

## Run the Example

We've included a comprehensive example script that demonstrates all SDK features:

```bash
python sdk/example.py
```

## Common Use Cases

### Get All Players

```python
players = client.list_players(limit=100)
for player in players:
    print(f"{player.first_name} {player.last_name} - {player.position}")
```

### Search for a Specific Player

```python
players = client.list_players(first_name="Tom", last_name="Brady")
if players:
    player = players[0]
    print(f"Found: {player.first_name} {player.last_name}")
```

### Get Player with Performances

```python
player = client.get_player(player_id=1)
print(f"{player.first_name} {player.last_name}")
print(f"Number of performances: {len(player.performances)}")

for perf in player.performances[:5]:  # Show first 5
    print(f"  Week {perf.week_number}: {perf.fantasy_points} points")
```

### Get League with Teams

```python
league = client.get_league(league_id=1)
print(f"{league.league_name} ({league.scoring_type})")
print(f"Number of teams: {len(league.teams)}")

for team in league.teams:
    print(f"  - {team.team_name}")
```

### Filter by Date

```python
from datetime import date

# Get players updated after a specific date
recent_players = client.list_players(
    min_last_changed_date=date(2024, 1, 1)
)
```

## Running Tests

To run the unit tests:

```bash
cd sdk
pytest -v
```

To run integration tests (requires API to be running):

```bash
pytest -v -m integration
```

## Next Steps

- Check out [README.md](README.md) for complete API documentation
- Explore the [example.py](example.py) script for more examples
- Review the [test_swcpy.py](test_swcpy.py) file for test examples

## Troubleshooting

### Import Errors

If you get import errors, make sure you've installed the SDK:
```bash
cd sdk
pip install -e .
```

### Connection Errors

If you get connection errors:
1. Make sure the API is running on http://localhost:8000
2. Check if you can access http://localhost:8000/ in your browser
3. Update the `swc_base_url` in your config if the API is on a different URL

### API Not Found Errors

If you get 404 errors:
1. Verify the API is running with the correct version
2. Check that the endpoints exist by visiting http://localhost:8000/docs

## Support

For more help, please refer to the main [README.md](README.md) or open an issue on GitHub.
