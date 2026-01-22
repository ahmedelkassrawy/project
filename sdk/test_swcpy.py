"""
Basic tests for the SWCPY SDK
"""
import pytest
from swcpy import SWCClient, SWCConfig
from datetime import date

@pytest.fixture
def client():
    """Create a test client"""
    config = SWCConfig(
        swc_base_url="http://localhost:8000",
        backoff=False,  # Disable backoff for faster tests
    )
    return SWCClient(config)

def test_config_initialization():
    """Test that config can be initialized with default values"""
    config = SWCConfig(swc_base_url="http://localhost:8000")
    assert config.swc_base_url == "http://localhost:8000"
    assert config.swc_backoff == True
    assert config.swc_backoff_max_time == 30
    assert config.swc_bulk_file_format == "csv"

def test_config_custom_values():
    """Test config with custom values"""
    config = SWCConfig(
        swc_base_url="http://example.com",
        backoff=False,
        backoff_max_time=60,
        bulk_file_format="parquet"
    )
    assert config.swc_base_url == "http://example.com"
    assert config.swc_backoff == False
    assert config.swc_backoff_max_time == 60
    assert config.swc_bulk_file_format == "parquet"

def test_client_initialization(client):
    """Test that client can be initialized"""
    assert client is not None
    assert client.swc_base_url == "http://localhost:8000"

# Integration tests (require running API)
@pytest.mark.integration
def test_health_check(client):
    """Test health check endpoint"""
    response = client.get_health_check()
    assert response is not None
    assert "message" in response

@pytest.mark.integration
def test_get_counts(client):
    """Test get counts endpoint"""
    counts = client.get_counts()
    assert counts is not None
    assert hasattr(counts, 'league_count')
    assert hasattr(counts, 'team_count')
    assert hasattr(counts, 'player_count')

@pytest.mark.integration
def test_list_players(client):
    """Test list players endpoint"""
    players = client.list_players(limit=10)
    assert isinstance(players, list)
    if len(players) > 0:
        player = players[0]
        assert hasattr(player, 'player_id')
        assert hasattr(player, 'first_name')
        assert hasattr(player, 'last_name')

@pytest.mark.integration
def test_list_leagues(client):
    """Test list leagues endpoint"""
    leagues = client.list_leagues(limit=10)
    assert isinstance(leagues, list)
    if len(leagues) > 0:
        league = leagues[0]
        assert hasattr(league, 'league_id')
        assert hasattr(league, 'league_name')

@pytest.mark.integration
def test_list_teams(client):
    """Test list teams endpoint"""
    teams = client.list_teams(limit=10)
    assert isinstance(teams, list)
    if len(teams) > 0:
        team = teams[0]
        assert hasattr(team, 'team_id')
        assert hasattr(team, 'team_name')

@pytest.mark.integration
def test_list_performances(client):
    """Test list performances endpoint"""
    performances = client.list_performances(limit=10)
    assert isinstance(performances, list)
    if len(performances) > 0:
        perf = performances[0]
        assert hasattr(perf, 'performance_id')
        assert hasattr(perf, 'fantasy_points')
