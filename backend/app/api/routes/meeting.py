from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, models
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[models.Meeting])
def read_meetings(db: Session = Depends(deps.get_db)):
    """Retrieve all meetings."""
    return crud.get_all_meetings(session=db)


@router.get("/{meeting_id}", response_model=models.Meeting)
def read_meeting(meeting_id: int, db: Session = Depends(deps.get_db)):
    """Retrieve a meeting by its ID."""
    meeting = crud.get_meeting(session=db, meeting_id=meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@router.post("/", response_model=models.Meeting)
def create_meeting(meeting_in: models.MeetingCreate, db: Session = Depends(deps.get_db)):
    """Create a new meeting."""
    return crud.create_meeting(session=db, meeting_in=meeting_in, owner_id=None)


@router.put("/{meeting_id}", response_model=models.Meeting)
def update_meeting(meeting_id: int, meeting_in: models.MeetingUpdate, db: Session = Depends(deps.get_db)):
    """Update an existing meeting."""
    meeting = crud.update_meeting(session=db, meeting_id=meeting_id, meeting_in=meeting_in)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@router.delete("/{meeting_id}", response_model=models.Meeting)
def delete_meeting(meeting_id: int, db: Session = Depends(deps.get_db)):
    """Delete a meeting."""
    meeting = crud.delete_meeting(session=db, meeting_id=meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting
