from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, date, timedelta
from backend.core.database import get_db
from backend.core.security import get_current_user
from backend.core.schemas import CheckboxUpdate, CheckboxOut, DashboardStats
from backend.models.models import CheckboxProgress, Goal, Streak, User

router = APIRouter(prefix="/api/progress", tags=["progress"])

@router.get("/", response_model=List[CheckboxOut])
def get_progress(
    week_number: Optional[int] = None,
    goal_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    q = db.query(CheckboxProgress).filter(CheckboxProgress.user_id == current_user.id)
    if week_number is not None:
        q = q.filter(CheckboxProgress.week_number == week_number)
    if goal_id is not None:
        q = q.filter(CheckboxProgress.goal_id == goal_id)
    return q.all()

@router.post("/checkbox", response_model=CheckboxOut)
def update_checkbox(data: CheckboxUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = db.query(Goal).filter(Goal.id == data.goal_id, Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    existing = db.query(CheckboxProgress).filter(
        CheckboxProgress.goal_id == data.goal_id,
        CheckboxProgress.user_id == current_user.id,
        CheckboxProgress.week_number == data.week_number,
        CheckboxProgress.day_of_week == data.day_of_week
    ).first()
    
    if existing:
        existing.completed = data.completed
        existing.completed_at = datetime.utcnow() if data.completed else None
        existing.date = data.date
        db.commit()
        db.refresh(existing)
        _update_streak(db, current_user.id, data.goal_id)
        return existing
    else:
        progress = CheckboxProgress(
            goal_id=data.goal_id,
            user_id=current_user.id,
            week_number=data.week_number,
            day_of_week=data.day_of_week,
            completed=data.completed,
            completed_at=datetime.utcnow() if data.completed else None,
            date=data.date
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
        _update_streak(db, current_user.id, data.goal_id)
        return progress

def _update_streak(db: Session, user_id: int, goal_id: int):
    completions = db.query(CheckboxProgress).filter(
        CheckboxProgress.user_id == user_id,
        CheckboxProgress.goal_id == goal_id,
        CheckboxProgress.completed == True,
        CheckboxProgress.date.isnot(None)
    ).order_by(CheckboxProgress.date.desc()).all()
    
    if not completions:
        return
    
    dates = sorted(set(c.date for c in completions), reverse=True)
    current = 1
    longest = 1
    for i in range(1, len(dates)):
        if (dates[i-1] - dates[i]).days == 1:
            current += 1
            longest = max(longest, current)
        else:
            break
    
    streak = db.query(Streak).filter(Streak.user_id == user_id, Streak.goal_id == goal_id).first()
    if streak:
        streak.current_streak = current
        streak.longest_streak = max(streak.longest_streak, longest)
        streak.last_completed = dates[0]
    else:
        streak = Streak(user_id=user_id, goal_id=goal_id, current_streak=current, longest_streak=longest, last_completed=dates[0])
        db.add(streak)
    db.commit()

@router.get("/dashboard-stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_goals = db.query(Goal).filter(Goal.user_id == current_user.id).count()
    active_goals = db.query(Goal).filter(Goal.user_id == current_user.id, Goal.is_active == True).count()
    
    today = date.today()
    today_completions = db.query(CheckboxProgress).filter(
        CheckboxProgress.user_id == current_user.id,
        CheckboxProgress.completed == True,
        CheckboxProgress.date == today
    ).count()
    
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    week_total = db.query(CheckboxProgress).filter(
        CheckboxProgress.user_id == current_user.id,
        CheckboxProgress.date >= week_start,
        CheckboxProgress.date <= week_end
    ).count()
    week_done = db.query(CheckboxProgress).filter(
        CheckboxProgress.user_id == current_user.id,
        CheckboxProgress.completed == True,
        CheckboxProgress.date >= week_start,
        CheckboxProgress.date <= week_end
    ).count()
    weekly_pct = round((week_done / week_total * 100) if week_total > 0 else 0, 1)
    
    streaks = db.query(Streak).filter(Streak.user_id == current_user.id).all()
    total_streak = sum(s.current_streak for s in streaks)
    
    total_completions = db.query(CheckboxProgress).filter(
        CheckboxProgress.user_id == current_user.id,
        CheckboxProgress.completed == True
    ).count()
    
    return DashboardStats(
        total_goals=total_goals,
        active_goals=active_goals,
        completed_today=today_completions,
        weekly_completion_pct=weekly_pct,
        total_streak=total_streak,
        total_completions=total_completions
    )

@router.get("/calendar")
def get_calendar_data(year: int, month: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from calendar import monthrange
    _, days_in_month = monthrange(year, month)
    result = {}
    active_goals = db.query(Goal).filter(Goal.user_id == current_user.id, Goal.is_active == True).count()
    
    for day in range(1, days_in_month + 1):
        d = date(year, month, day)
        if d > date.today():
            result[str(d)] = "future"
            continue
        done = db.query(CheckboxProgress).filter(
            CheckboxProgress.user_id == current_user.id,
            CheckboxProgress.completed == True,
            CheckboxProgress.date == d
        ).count()
        total = db.query(CheckboxProgress).filter(
            CheckboxProgress.user_id == current_user.id,
            CheckboxProgress.date == d
        ).count()
        if total == 0:
            result[str(d)] = "none"
        elif done == total and done > 0:
            result[str(d)] = "complete"
        elif done > 0:
            result[str(d)] = "partial"
        else:
            result[str(d)] = "missed"
    return result

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from collections import defaultdict
    
    all_progress = db.query(CheckboxProgress).filter(
        CheckboxProgress.user_id == current_user.id,
        CheckboxProgress.date.isnot(None)
    ).all()
    
    weekly_data = defaultdict(lambda: {"completed": 0, "total": 0})
    category_data = defaultdict(lambda: {"completed": 0, "total": 0})
    daily_heatmap = defaultdict(int)
    
    goals_map = {g.id: g for g in db.query(Goal).filter(Goal.user_id == current_user.id).all()}
    
    for p in all_progress:
        week_key = f"W{p.week_number}"
        weekly_data[week_key]["total"] += 1
        daily_heatmap[str(p.date)] += (1 if p.completed else 0)
        if p.completed:
            weekly_data[week_key]["completed"] += 1
        
        goal = goals_map.get(p.goal_id)
        if goal:
            category_data[goal.category]["total"] += 1
            if p.completed:
                category_data[goal.category]["completed"] += 1
    
    streaks = db.query(Streak).filter(Streak.user_id == current_user.id).all()
    streak_data = []
    for s in streaks:
        goal = goals_map.get(s.goal_id)
        if goal:
            streak_data.append({"goal": goal.title, "current": s.current_streak, "longest": s.longest_streak})
    
    return {
        "weekly": dict(weekly_data),
        "categories": dict(category_data),
        "heatmap": dict(daily_heatmap),
        "streaks": streak_data
    }
