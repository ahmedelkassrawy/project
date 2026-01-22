import httpx
import swcpy.swc_config as config
from .schemas.schemas import League, Team, Player, Performance, Counts
from typing import List, Optional
from datetime import date
import backoff
import logging

logger = logging.getLogger(__name__)

class SWCClient:
    HEALTH_CHECK_ENDPOINT = "/" 
    LIST_LEAGUES_ENDPOINT = "/v0/leagues/"
    LIST_PLAYERS_ENDPOINT = "/v0/players/"
    LIST_PERFORMANCES_ENDPOINT = "/v0/performances/"
    LIST_TEAMS_ENDPOINT = "/v0/teams/"
    GET_COUNTS_ENDPOINT = "/v0/counts/"

    BULK_FILE_BASE_URL = ""

    def __init__(self, input_config: config.SWCConfig):
        logger.debug(f"Bulk file base URL: {self.BULK_FILE_BASE_URL}")
        logger.debug(f"Input config: {input_config}")

        self.swc_base_url = input_config.swc_base_url
        self.backoff_enabled = input_config.swc_backoff
        self.backoff_max_time = input_config.swc_backoff_max_time
        self.bulk_file_format = input_config.swc_bulk_file_format
        self.BULK_FILE_NAMES = { 
            "players": "player_data",
            "leagues": "league_data",
            "performances": "performance_data",
            "teams": "team_data",
            "team_players": "team_player_data",
        }

        if self.backoff_enabled: 
            self.call_api = backoff.on_exception(
                wait_gen=backoff.expo,
                exception=(httpx.RequestError, httpx.HTTPStatusError),
                max_time=self.backoff_max_time,
                jitter=backoff.random_jitter,
            )(self._call_api)
        else:
            self.call_api = self._call_api

        if self.bulk_file_format.lower() == "parquet":
            self.BULK_FILE_NAMES = {
                key: value + ".parquet" for key, value in
                self.BULK_FILE_NAMES.items()
            }
        else:
            self.BULK_FILE_NAMES = {
                key: value + ".csv" for key, value in
                self.BULK_FILE_NAMES.items()
            }
        logger.debug(f"Bulk file dictionary: {self.BULK_FILE_NAMES}")

    def _call_api(self, method: str, endpoint: str, params: dict = None):
        """Internal method to make API calls."""
        with httpx.Client(base_url=self.swc_base_url, timeout=30.0) as client:
            response = client.request(method, endpoint, params=params)
            response.raise_for_status()
            return response.json()

    def get_health_check(self) -> dict:
        """Check the health of the API."""
        return self.call_api("GET", self.HEALTH_CHECK_ENDPOINT)
    
    def get_counts(self) -> Counts:
        """Get counts of leagues, teams, and players."""
        data = self.call_api("GET", self.GET_COUNTS_ENDPOINT)
        return Counts(**data)
    
    def list_players(
        self, 
        skip: int = 0, 
        limit: int = 100,
        min_last_changed_date: Optional[date] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> List[Player]:
        """List players with optional filters."""
        params = {"skip": skip, "limit": limit}
        if min_last_changed_date:
            params["min_last_changed_date"] = min_last_changed_date.isoformat()
        if first_name:
            params["first_name"] = first_name
        if last_name:
            params["last_name"] = last_name
        
        data = self.call_api("GET", self.LIST_PLAYERS_ENDPOINT, params=params)
        return [Player(**player) for player in data]
    
    def get_player(self, player_id: int) -> Player:
        """Get a specific player by ID."""
        endpoint = f"/v0/players/{player_id}"
        data = self.call_api("GET", endpoint)
        return Player(**data)
    
    def list_performances(
        self,
        skip: int = 0,
        limit: int = 100,
        min_last_changed_date: Optional[date] = None
    ) -> List[Performance]:
        """List performances with optional filters."""
        params = {"skip": skip, "limit": limit}
        if min_last_changed_date:
            params["min_last_changed_date"] = min_last_changed_date.isoformat()
        
        data = self.call_api("GET", self.LIST_PERFORMANCES_ENDPOINT, params=params)
        return [Performance(**perf) for perf in data]
    
    def get_performance(self, performance_id: int) -> Performance:
        """Get a specific performance by ID."""
        endpoint = f"/v0/performances/{performance_id}"
        data = self.call_api("GET", endpoint)
        return Performance(**data)
    
    def list_leagues(
        self,
        skip: int = 0,
        limit: int = 100,
        min_last_changed_date: Optional[date] = None,
        league_name: Optional[str] = None
    ) -> List[League]:
        """List leagues with optional filters."""
        params = {"skip": skip, "limit": limit}
        if min_last_changed_date:
            params["min_last_changed_date"] = min_last_changed_date.isoformat()
        if league_name:
            params["league_name"] = league_name
        
        data = self.call_api("GET", self.LIST_LEAGUES_ENDPOINT, params=params)
        return [League(**league) for league in data]
    
    def get_league(self, league_id: int) -> League:
        """Get a specific league by ID."""
        endpoint = f"/v0/leagues/{league_id}"
        data = self.call_api("GET", endpoint)
        return League(**data)
    
    def list_teams(
        self,
        skip: int = 0,
        limit: int = 100,
        min_last_changed_date: Optional[date] = None,
        team_name: Optional[str] = None,
        league_id: Optional[int] = None
    ) -> List[Team]:
        """List teams with optional filters."""
        params = {"skip": skip, "limit": limit}
        if min_last_changed_date:
            params["min_last_changed_date"] = min_last_changed_date.isoformat()
        if team_name:
            params["team_name"] = team_name
        if league_id:
            params["league_id"] = league_id
        
        data = self.call_api("GET", self.LIST_TEAMS_ENDPOINT, params=params)
        return [Team(**team) for team in data]
    
    def get_team(self, team_id: int) -> Team:
        """Get a specific team by ID."""
        endpoint = f"/v0/teams/{team_id}"
        data = self.call_api("GET", endpoint)
        return Team(**data)