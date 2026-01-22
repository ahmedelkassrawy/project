# SWCPY - Python SDK for SWC Fantasy Sports API

A Python SDK for interacting with the SWC Fantasy Sports API.

## Installation

```bash
cd sdk
pip install -e .
```

## Quick Start

```python
from swcpy import SWCClient, SWCConfig

# Initialize the client
config = SWCConfig(
    swc_base_url="http://localhost:8000",
    backoff=True,  # Enable automatic retry with exponential backoff
    backoff_max_time=30,  # Maximum time to retry in seconds
    bulk_file_format="csv"
)

client = SWCClient(config)

# Check API health
health = client.get_health_check()
print(health)
```

## Features

- Full coverage of all SWC API endpoints
- Type-safe with Pydantic models
- Automatic retry with exponential backoff
- Support for filtering and pagination
- Python 3.10+ support

## API Methods

### Health Check

```python
# Check if the API is running
health = client.get_health_check()
```

### Counts

```python
# Get counts of all entities
counts = client.get_counts()
print(f"Leagues: {counts.league_count}")
print(f"Teams: {counts.team_count}")
print(f"Players: {counts.player_count}")
```

### Players

```python
# List all players with pagination
players = client.list_players(skip=0, limit=100)

# Filter players by name
players = client.list_players(first_name="John", last_name="Smith")

# Filter by last changed date
from datetime import date
players = client.list_players(
    min_last_changed_date=date(2024, 1, 1)
)

# Get a specific player by ID
player = client.get_player(player_id=1)
print(f"{player.first_name} {player.last_name} - {player.position}")
print(f"Performances: {len(player.performances)}")
```

### Performances

```python
# List all performances
performances = client.list_performances(skip=0, limit=100)

# Filter by last changed date
performances = client.list_performances(
    min_last_changed_date=date(2024, 1, 1)
)

# Get a specific performance by ID
performance = client.get_performance(performance_id=1)
print(f"Week {performance.week_number}: {performance.fantasy_points} points")
```

### Leagues

```python
# List all leagues
leagues = client.list_leagues(skip=0, limit=100)

# Filter by league name
leagues = client.list_leagues(league_name="Premier League")

# Get a specific league by ID
league = client.get_league(league_id=1)
print(f"{league.league_name} - {league.scoring_type}")
print(f"Teams: {len(league.teams)}")
```

### Teams

```python
# List all teams
teams = client.list_teams(skip=0, limit=100)

# Filter by team name
teams = client.list_teams(team_name="Champions")

# Filter by league
teams = client.list_teams(league_id=1)

# Get a specific team by ID
team = client.get_team(team_id=1)
print(f"{team.team_name}")
print(f"Players: {len(team.players)}")
```

## Configuration Options

The `SWCConfig` class supports the following options:

- `swc_base_url` (str): Base URL of the API (required)
- `backoff` (bool): Enable automatic retry with exponential backoff (default: True)
- `backoff_max_time` (int): Maximum time to retry in seconds (default: 30)
- `bulk_file_format` (str): Format for bulk file downloads - "csv" or "parquet" (default: "csv")

## Error Handling

The SDK will raise `httpx.HTTPStatusError` for HTTP errors. You can handle them like this:

```python
import httpx

try:
    player = client.get_player(player_id=999999)
except httpx.HTTPStatusError as e:
    if e.response.status_code == 404:
        print("Player not found")
    else:
        print(f"Error: {e}")
```

## Advanced Usage

### Using Environment Variables

You can use environment variables for configuration:

```python
import os
from swcpy import SWCClient, SWCConfig

config = SWCConfig(
    swc_base_url=os.getenv("SWC_BASE_URL", "http://localhost:8000")
)
client = SWCClient(config)
```

### Combining Filters

```python
from datetime import date

# Get all quarterbacks named "Tom" who were updated after a certain date
players = client.list_players(
    first_name="Tom",
    min_last_changed_date=date(2024, 1, 1),
    skip=0,
    limit=50
)

for player in players:
    if player.position == "QB":
        print(f"{player.first_name} {player.last_name}")
```

### Iterating Through All Records

```python
# Get all players using pagination
all_players = []
skip = 0
limit = 100

while True:
    players = client.list_players(skip=skip, limit=limit)
    if not players:
        break
    all_players.extend(players)
    skip += limit

print(f"Total players: {len(all_players)}")
```

## Development

### Running Tests

```bash
cd sdk
pip install -e ".[dev]"
pytest
```

## License

MIT License

## Support

For issues and questions, please open an issue on the GitHub repository.
