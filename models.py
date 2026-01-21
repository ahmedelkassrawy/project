#define the sqlalchemy models here
from sqlalchemy import Column, Integer, ForeignKey, String, DATETIME
from sqlalchemy.orm import relationship
from database import Base

class Player(Base):
    __tablename__ = "player"
    
    player_id = Column(Integer, primary_key=True, nullable=False)
    gsis_id = Column(String, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    last_changed_date = Column(DATETIME, nullable=False)

    performances = relationship("Performance", back_populates="player")

    # Many-to-Many relationship through the association table
    teams = relationship("Team", secondary="team_player", back_populates="players")
    
    # Direct access to the link table records (Association Object pattern)
    team_links = relationship("TeamPlayer", back_populates="player", viewonly=True)

class Team(Base):
    __tablename__ = "team"

    team_id = Column(Integer, primary_key=True, nullable=False)
    team_name = Column(String, nullable=False)
    league_id = Column(Integer, ForeignKey("league.league_id"), nullable=False)
    last_changed_date = Column(DATETIME, nullable=False)

    league = relationship("League", back_populates="teams")
    players = relationship("Player", secondary="team_player", back_populates="teams")
    
    # Direct access to the link table records
    player_links = relationship("TeamPlayer", back_populates="team", viewonly=True)

class Performance(Base):
    __tablename__ = "performance"

    performance_id = Column(Integer, primary_key=True, nullable=False)
    week_number = Column(String, nullable=False)
    fantasy_points = Column(Integer, nullable=False)
    player_id = Column(Integer, ForeignKey("player.player_id"), nullable=False)
    last_changed_date = Column(DATETIME, nullable=False)

    player = relationship("Player", back_populates="performances")

class League(Base):
    __tablename__ = "league"

    league_id = Column(Integer, primary_key=True, nullable=False)
    league_name = Column(String, nullable=False)
    scoring_type = Column(String, nullable=False)
    last_changed_date = Column(DATETIME, nullable=False)

    teams = relationship("Team", back_populates="league")

class TeamPlayer(Base):
    __tablename__ = "team_player"

    team_id = Column(Integer, ForeignKey("team.team_id"), primary_key=True, nullable=False)
    player_id = Column(Integer, ForeignKey("player.player_id"), primary_key=True, nullable=False)
    last_changed_date = Column(DATETIME, nullable=False)

    # We map back to the 'links' attributes to avoid clashing with 'players' and 'teams'
    team = relationship("Team", back_populates="player_links")
    player = relationship("Player", back_populates="team_links")