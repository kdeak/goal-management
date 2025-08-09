import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    Boolean,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    okrs = relationship("OKR", back_populates="user")


class OKR(Base):
    __tablename__ = "okrs"
    id = Column(Integer, primary_key=True)
    objective = Column(String, nullable=False)
    timeframe_start = Column(Date)
    timeframe_end = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="okrs")
    key_results = relationship("KeyResult", back_populates="okr", cascade="all, delete-orphan")
    smart_goals = relationship("SMARTGoal", back_populates="okr", cascade="all, delete-orphan")


class KeyResult(Base):
    __tablename__ = "key_results"
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    target_value = Column(Float)
    current_value = Column(Float, default=0.0)
    unit = Column(String)
    okr_id = Column(Integer, ForeignKey("okrs.id"), nullable=False)
    okr = relationship("OKR", back_populates="key_results")


class SMARTGoal(Base):
    __tablename__ = "smart_goals"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specific = Column(String)
    measurable = Column(String)
    achievable = Column(String)
    relevant = Column(String)
    time_bound = Column(Date)
    okr_id = Column(Integer, ForeignKey("okrs.id"), nullable=False)
    okr = relationship("OKR", back_populates="smart_goals")
    tasks = relationship("Task", back_populates="smart_goal", cascade="all, delete-orphan")


class TaskSize(enum.Enum):
    BIG = 1
    MEDIUM = 3
    SMALL = 5


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    size = Column(Enum(TaskSize), nullable=False)
    date = Column(Date, nullable=False)
    completed = Column(Boolean, default=False)
    smart_goal_id = Column(Integer, ForeignKey("smart_goals.id"), nullable=False)
    smart_goal = relationship("SMARTGoal", back_populates="tasks")
