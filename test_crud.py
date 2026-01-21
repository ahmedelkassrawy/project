#the pytest for unit test of the db
import pytest
from datetime import date, datetime
import csv
import os
import crud
from database import SessionLocal, engine, Base
import models

#test date set to before data dates (2024) to ensure data is returned
test_date = date(2023, 1, 1)

def load_data(session):
    print("Loading data from CSVs...")
    # Leagues
    if os.path.exists('data/league_data.csv'):
        with open('data/league_data.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                session.merge(models.League(
                    league_id=int(row['league_id']),
                    league_name=row['league_name'],
                    scoring_type=row['scoring_type'],
                    last_changed_date=datetime.strptime(row['last_changed_date'], '%Y-%m-%d')
                ))
            
    # Teams
    if os.path.exists('data/team_data.csv'):
        with open('data/team_data.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                session.merge(models.Team(
                    team_id=int(row['team_id']),
                    team_name=row['team_name'],
                    league_id=int(row['league_id']),
                    last_changed_date=datetime.strptime(row['last_changed_date'], '%Y-%m-%d')
                ))

    # Players
    if os.path.exists('data/player_data.csv'):
        with open('data/player_data.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                session.merge(models.Player(
                    player_id=int(row['player_id']),
                    gsis_id=row['gsis_id'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    position=row['position'],
                    last_changed_date=datetime.strptime(row['last_changed_date'], '%Y-%m-%d')
                ))
            
    # TeamPlayer
    if os.path.exists('data/team_player_data.csv'):
        with open('data/team_player_data.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                session.merge(models.TeamPlayer(
                    team_id=int(row['team_id']),
                    player_id=int(row['player_id']),
                    last_changed_date=datetime.strptime(row['last_changed_date'], '%Y-%m-%d')
                ))

    # Performance
    if os.path.exists('data/performance_data.csv'):
        with open('data/performance_data.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                session.merge(models.Performance(
                    performance_id=int(row['performance_id']),
                    week_number=row['week_number'],
                    fantasy_points=int(row['fantasy_points']),
                    player_id=int(row['player_id']),
                    last_changed_date=datetime.strptime(row['last_changed_date'], '%Y-%m-%d')
                ))
    
    session.commit()
    print("Data loaded.")

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    # Check if data exists, if not load it
    if session.query(models.Player).count() == 0:
        load_data(session)
    session.close()

@pytest.fixture(scope = "function")
def db_session():
    """Start db session and closes it after test"""
    session = SessionLocal()
    yield session
    session.close()

def test_get_player(db_session):
    player = crud.get_player(db_session, player_id = 1001)
    assert player is not None
    assert player.player_id == 1001

def test_get_players(db_session):
    # increased limit to get all players
    players = crud.get_players(db_session,skip = 0, limit=2000,
                               min_last_changed_date = test_date,)
    # Based on wc -l data/player_data.csv is 1018lines.
    # User original test expected 1018.
    assert len(players) == 1018

def test_get_players_by_name(db_session):
    # 2009 is Bryce Young. 
    players = crud.get_players(db_session,first_name = "Bryce")

    assert len(players) > 0
    ids = [p.player_id for p in players]
    assert 2009 in ids

def test_get_all_performances(db_session):
    # increased limit
    performances = crud.get_performances(db_session,skip = 0, limit=20000,
                                        min_last_changed_date = test_date)
    # wc -l says 17307 lines -> 17306 records
    assert len(performances) == 17306

def test_get_player_count(db_session):
    player_count = crud.get_player_count(db_session)
    assert player_count == 1018
