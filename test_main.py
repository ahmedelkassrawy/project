from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#test the health check endpoint
def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "API health check successful"}

#test the read_players endpoint
def test_read_players():
    response = client.get("/v0/players/?skip=0&limit=2000")

    assert response.status_code == 200
    assert len(response.json()) == 1018

# test /v0/players/{player_id}/
def test_read_players_with_id():
    response = client.get("/v0/players/1001/")

    assert response.status_code == 200
    assert response.json().get("player_id") == 1001

# test /v0/performances/
def test_read_performances():
    response = client.get("/v0/performances/?skip=0&limit=20000")
    assert response.status_code == 200
    assert len(response.json()) == 17306

# test /v0/leagues/{league_id}/
def test_read_leagues_with_id():
    response = client.get("/v0/leagues/5002/")
    assert response.status_code == 200
    assert len(response.json()["teams"]) == 8

# test the count functions
def test_counts():
    response = client.get("/v0/counts/")

    assert response.status_code == 200
    assert response.json()["league_count"] == 5
    assert response.json()["team_count"] == 20
    assert response.json()["player_count"] == 1018