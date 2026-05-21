from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.core.database import get_db
from backend.core.security import get_current_user
from backend.core.schemas import GoalCreate, GoalUpdate, GoalOut
from backend.models.models import Goal, User

router = APIRouter(prefix="/api/goals", tags=["goals"])

@router.get("/", response_model=List[GoalOut])
def get_goals(
    search: Optional[str] = None,
    category: Optional[str] = None,
    priority: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    q = db.query(Goal).filter(Goal.user_id == current_user.id)
    if search:
        q = q.filter(Goal.title.ilike(f"%{search}%"))
    if category:
        q = q.filter(Goal.category == category)
    if priority:
        q = q.filter(Goal.priority == priority)
    if is_active is not None:
        q = q.filter(Goal.is_active == is_active)
    return q.order_by(Goal.created_at.desc()).all()

@router.post("/", response_model=GoalOut)
def create_goal(goal_data: GoalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = Goal(user_id=current_user.id, **goal_data.model_dump())
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal

@router.put("/{goal_id}", response_model=GoalOut)
def update_goal(goal_id: int, goal_data: GoalUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    for k, v in goal_data.model_dump(exclude_unset=True).items():
        setattr(goal, k, v)
    db.commit()
    db.refresh(goal)
    return goal

@router.delete("/{goal_id}")
def delete_goal(goal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(goal)
    db.commit()
    return {"message": "Goal deleted"}
