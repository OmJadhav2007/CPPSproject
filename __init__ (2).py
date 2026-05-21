from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import csv, io
from backend.core.database import get_db
from backend.core.security import get_current_user
from backend.models.models import Goal, CheckboxProgress, Note, User

router = APIRouter(prefix="/api/export", tags=["export"])

@router.get("/csv")
def export_csv(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Type", "ID", "Title/Goal", "Category", "Week", "Day", "Completed", "Date", "Notes"])
    
    goals = db.query(Goal).filter(Goal.user_id == current_user.id).all()
    for goal in goals:
        writer.writerow(["Goal", goal.id, goal.title, goal.category, "", "", goal.is_active, goal.start_date, goal.notes])
    
    progress = db.query(CheckboxProgress).filter(CheckboxProgress.user_id == current_user.id).all()
    goal_map = {g.id: g.title for g in goals}
    for p in progress:
        writer.writerow(["Progress", p.id, goal_map.get(p.goal_id, ""), "", p.week_number, p.day_of_week, p.completed, p.date, ""])
    
    notes = db.query(Note).filter(Note.user_id == current_user.id).all()
    for note in notes:
        writer.writerow(["Note", note.id, note.title, "", "", "", "", note.created_at, note.content[:100]])
    
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=goal_sync_export.csv"}
    )
