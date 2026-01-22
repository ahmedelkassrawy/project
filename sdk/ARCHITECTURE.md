# SDK Architecture

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Your Application                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ imports
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                         SWCPY SDK                            │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  SWCClient                                           │  │
│  │  ┌───────────────────────────────────────────────┐  │  │
│  │  │ • list_players()                              │  │  │
│  │  │ • get_player(id)                              │  │  │
│  │  │ • list_performances()                         │  │  │
│  │  │ • get_performance(id)                         │  │  │
│  │  │ • list_leagues()                              │  │  │
│  │  │ • get_league(id)                              │  │  │
│  │  │ • list_teams()                                │  │  │
│  │  │ • get_team(id)                                │  │  │
│  │  │ • get_counts()                                │  │  │
│  │  │ • get_health_check()                          │  │  │
│  │  └───────────────────────────────────────────────┘  │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────┴───────────────────────────────┐  │
│  │  SWCConfig                                           │  │
│  │  ┌───────────────────────────────────────────────┐  │  │
│  │  │ • swc_base_url                                │  │  │
│  │  │ • swc_backoff                                 │  │  │
│  │  │ • swc_backoff_max_time                        │  │  │
│  │  │ • swc_bulk_file_format                        │  │  │
│  │  └───────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Schemas (Pydantic Models)                           │  │
│  │  ┌───────────────────────────────────────────────┐  │  │
│  │  │ • Player                                      │  │  │
│  │  │ • PlayerBase                                  │  │  │
│  │  │ • Performance                                 │  │  │
│  │  │ • Team                                        │  │  │
│  │  │ • TeamBase                                    │  │  │
│  │  │ • League                                      │  │  │
│  │  │ • Counts                                      │  │  │
│  │  └───────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP Requests (httpx)
                         │ with Backoff Retry
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    SWC Fantasy Sports API                    │
│                                                              │
│  FastAPI Application                                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ GET /                        - Health Check          │  │
│  │ GET /v0/counts/              - Get Counts            │  │
│  │ GET /v0/players/             - List Players          │  │
│  │ GET /v0/players/{id}         - Get Player            │  │
│  │ GET /v0/performances/        - List Performances     │  │
│  │ GET /v0/performances/{id}    - Get Performance       │  │
│  │ GET /v0/leagues/             - List Leagues          │  │
│  │ GET /v0/leagues/{id}         - Get League            │  │
│  │ GET /v0/teams/               - List Teams            │  │
│  │ GET /v0/teams/{id}           - Get Team              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

```
User Code
    │
    │ 1. Create Config
    ▼
config = SWCConfig(swc_base_url="...")
    │
    │ 2. Initialize Client
    ▼
client = SWCClient(config)
    │
    │ 3. Make API Call
    ▼
players = client.list_players(limit=10)
    │
    │ 4. HTTP Request
    ▼
[SDK sends GET request to /v0/players/?limit=10]
    │
    │ 5. Retry on Error (if backoff enabled)
    ▼
[Exponential backoff if request fails]
    │
    │ 6. Receive JSON Response
    ▼
[API returns JSON array of players]
    │
    │ 7. Parse & Validate
    ▼
[Pydantic models validate data]
    │
    │ 8. Return Type-Safe Objects
    ▼
List[Player] returned to user
```

## SDK Files

```
sdk/
│
├── pyproject.toml              # Package definition & dependencies
├── pytest.ini                  # Pytest configuration
├── .gitignore                 # Git ignore rules
│
├── README.md                   # Complete documentation
├── QUICKSTART.md              # Quick start guide
├── SDK_SUMMARY.md             # This file
│
├── example.py                  # Usage examples
├── test_swcpy.py              # Test suite
│
└── ../src/swcpy/              # Source code
    ├── __init__.py            # Package initialization & exports
    ├── swc_client.py          # Main SDK client (200+ lines)
    ├── swc_config.py          # Configuration class
    └── schemas/
        └── schemas.py         # Pydantic data models
```

## Usage Pattern

```python
# 1. Import
from swcpy import SWCClient, SWCConfig

# 2. Configure
config = SWCConfig(
    swc_base_url="http://localhost:8000",
    backoff=True,
    backoff_max_time=30
)

# 3. Initialize
client = SWCClient(config)

# 4. Use any method
players = client.list_players(limit=10)
player = client.get_player(player_id=1)
leagues = client.list_leagues()
counts = client.get_counts()
```

## Testing Strategy

```
Unit Tests
    │
    ├── test_config_initialization()
    ├── test_config_custom_values()
    └── test_client_initialization()

Integration Tests (require running API)
    │
    ├── test_health_check()
    ├── test_get_counts()
    ├── test_list_players()
    ├── test_list_leagues()
    ├── test_list_teams()
    └── test_list_performances()
```

## Error Handling

```
User calls method
    │
    ▼
SDK makes HTTP request
    │
    ├─ Success → Parse JSON → Validate with Pydantic → Return
    │
    ├─ Network Error → Retry with backoff (if enabled) → Success/Fail
    │
    ├─ 404 Not Found → Raise HTTPStatusError
    │
    └─ 500 Server Error → Retry with backoff → Raise HTTPStatusError
```

## Key Features Implemented

✅ **Complete API Coverage**: All 10 API endpoints
✅ **Type Safety**: Pydantic models for validation
✅ **Retry Logic**: Exponential backoff with jitter
✅ **Filtering**: Support for all query parameters
✅ **Pagination**: Skip/limit parameters
✅ **Date Filtering**: min_last_changed_date support
✅ **Documentation**: README, Quick Start, Examples
✅ **Testing**: Unit and integration tests
✅ **Error Handling**: Proper exception handling
✅ **Developer Experience**: Clear API, good defaults

## Installation & Usage Summary

```bash
# Install
cd sdk && pip install -e .

# Use
python example.py

# Test
pytest -v

# Test with API running
pytest -v -m integration
```

That's it! The SDK is complete and ready to use. 🎉
