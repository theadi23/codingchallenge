from sqlmodel import Session
from app.models import Meeting, User
import uuid


def create_random_meeting(db: Session) -> Meeting:
    fake_owner_id = uuid.uuid4()  # Replace with a real user ID if necessary
    meeting = Meeting(
        title="Random Meeting",
        agenda="Random Agenda",
        summary="Random Summary",
        owner_id=fake_owner_id,
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting
