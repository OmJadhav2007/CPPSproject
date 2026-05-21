from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime

# Auth
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

# Goals
class GoalCreate(BaseModel):
    title: str
    category: str = "Custom"
    priority: str = "Medium"
    notes: str = ""
    start_date: Optional[date] = None
    target_frequency: str = "Daily"

class GoalUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    notes: Optional[str] = None
    target_frequency: Optional[str] = None
    is_active: Optional[bool] = None

class GoalOut(BaseModel):
    id: int
    title: str
    category: str
    priority: str
    notes: str
    start_date: Optional[date]
    target_frequency: str
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

# Checkbox Progress
class CheckboxUpdate(BaseModel):
    goal_id: int
    week_number: int
    day_of_week: str
    completed: bool
    date: Optional[date] = None

class CheckboxOut(BaseModel):
    id: int
    goal_id: int
    week_number: int
    day_of_week: str
    completed: bool
    completed_at: Optional[datetime]
    date: Optional[date]
    class Config:
        from_attributes = True

# Notes
class NoteCreate(BaseModel):
    title: str = "Untitled Note"
    content: str = ""

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# Analytics
class DashboardStats(BaseModel):
    total_goals: int
    active_goals: int
    completed_today: int
    weekly_completion_pct: float
    total_streak: int
    total_completions: int
