from fastapi import Depends,FastAPI,HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date 
import crud,schemas 
from database import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/",tags = ["analytics"])
async def root():
    return {"message": "API health check successful"}

@app.get("/v0/players/", response_model = list[schemas.Player],
         tags = ["player"])
def read_players(skip:int = Query(0,description = "The skip at the beginning of API call"), 
                 limit:int = Query(100,description = "The maximum number of players to return"),
                 min_last_changed_date: date = None,
                 first_name: str = None, last_name: str = None,
                 db:Session = Depends(get_db)):
    players = crud.get_players(db,skip = skip, limit = limit,
                               min_last_changed_date = min_last_changed_date,
                               first_name = first_name,
                               last_name = last_name)
    return players

@app.get("/v0/players/{player_id}",
        response_model = schemas.Player,
        tags = ["player"],summary = "Get player by ID",
        description="Retrieve a player's details using their unique player ID.",
        response_description="A JSON object containing the player's details.",
        operation_id="getPlayerById")
def read_player(db:Session = Depends(get_db), player_id:int = None):
    player = crud.get_player(db, player_id = player_id)

    if player is None:
        raise HTTPException(status_code = 404, 
                            detail = "Player not found")
    return player

@app.get("/v0/performances/", response_model = list[schemas.Performance],
         tags = ["scoring"])
def read_performances(db:Session = Depends(get_db),
                      skip:int = 0, limit:int = 100,
                      min_last_changed_date: date = None):
    performances = crud.get_performances(db, skip = skip,
                                        limit = limit,
                                        min_last_changed_date = min_last_changed_date)
    return performances

@app.get("/v0/performances/{performance_id}", response_model = schemas.Performance,
        tags = ["scoring"])
def read_performance(db:Session = Depends(get_db), performance_id:int = None):
    performance = crud.get_performance(db, performance_id = performance_id)

    if performance is None:
        raise HTTPException(status_code = 404,
                            detail = "Performance not found")
    return performance

@app.get("/v0/leagues/", response_model = list[schemas.League],
         tags = ["membership"])
def read_leagues(db:Session = Depends(get_db),
                    skip:int = 0, limit:int = 100,
                    min_last_changed_date: date = None,
                    league_name: str = None):
        leagues = crud.get_leagues(db, skip = skip,
                                limit = limit,
                                min_last_changed_date = min_last_changed_date,
                                league_name = league_name)
        return leagues

@app.get("/v0/leagues/{league_id}", response_model = schemas.League,
         tags = ["membership"])
def read_league(db:Session = Depends(get_db), league_id: int = None):
    league = crud.get_league(db,league_id = league_id)

    if league is None:
        raise HTTPException(status_code = 404,
                            detail = "League not found")
    return league

@app.get("/v0/teams/", response_model = list[schemas.Team],
         tags=["membership"])
def read_teams(db:Session = Depends(get_db), skip:int=0, limit:int=100,
              min_last_changed_date:date = None,
              team_name:str = None,
              league_id:int = None):
    teams = crud.get_teams(db, skip = skip,
                           limit = limit,
                           min_last_changed_date = min_last_changed_date,
                           team_name = team_name,
                           league_id = league_id)
    return teams

@app.get("/v0/teams/{team_id}", response_model = schemas.Team,
         tags = ["membership"])
def read_team(db:Session = Depends(get_db), team_id:int = None):
    team = crud.get_team(db, team_id = team_id)

    if team is None:
        raise HTTPException(status_code = 404,
                            detail = "Team not found")
    return team

@app.get("/v0/counts/", response_model = schemas.Counts,
         tags = ["analytics"])
def read_counts(db:Session = Depends(get_db)):
    leagues_count = crud.get_league_count(db)
    teams_count = crud.get_team_count(db)
    players_count = crud.get_player_count(db)

    counts = schemas.Counts(
        league_count = leagues_count,
        team_count = teams_count,
        player_count = players_count
    )
    return counts