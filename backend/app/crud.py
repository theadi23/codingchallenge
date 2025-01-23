import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import Item, ItemCreate, User, UserCreate, UserUpdate, Meeting, MeetingCreate, MeetingUpdate
from typing import Optional


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def create_meeting(*, session: Session, meeting_in: MeetingCreate, owner_id: Optional[uuid.UUID] = None) -> Meeting:
    meeting_data = meeting_in.dict()
    meeting_data["owner_id"] = owner_id  # Explicitly add the owner_id (can be None)
    
    db_meeting = Meeting(**meeting_data)
    session.add(db_meeting)
    session.commit()
    session.refresh(db_meeting)
    return db_meeting


def get_meeting(*, session: Session, meeting_id: int) -> Meeting | None:
    statement = select(Meeting).where(Meeting.id == meeting_id)
    return session.exec(statement).first()


def get_all_meetings(*, session: Session) -> list[Meeting]:
    statement = select(Meeting)
    return session.exec(statement).all()


def update_meeting(*, session: Session, meeting_id: int, meeting_in: MeetingUpdate) -> Meeting | None:
    db_meeting = get_meeting(session=session, meeting_id=meeting_id)
    if not db_meeting:
        return None
    meeting_data = meeting_in.model_dump(exclude_unset=True)
    db_meeting.sqlmodel_update(meeting_data)
    session.add(db_meeting)
    session.commit()
    session.refresh(db_meeting)
    return db_meeting


def delete_meeting(*, session: Session, meeting_id: int) -> Meeting | None:
    db_meeting = get_meeting(session=session, meeting_id=meeting_id)
    if not db_meeting:
        return None
    session.delete(db_meeting)
    session.commit()
    return db_meeting
