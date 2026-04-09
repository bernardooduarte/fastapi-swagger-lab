from typing import List

from fastapi import Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import UserDB
from app.repositories.base import Repository

class UserRepository(Repository[UserDB]):

    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, db_obj: UserDB) -> UserDB:
        return UserDB(
            id=db_obj.id,
            username=db_obj.username,
            password_hash=db_obj.password_hash,
        )
    
    def get_user_by_username(self, username: str) -> UserDB:
        statement = select(UserDB).where(UserDB.username == username)
        db_obj = self.session.exec(statement).first()
        if not db_obj:
            raise ValueError("User not found")
        return self._to_domain(db_obj)

    def get(self, id: int) -> UserDB:
        statement = select(UserDB).where(UserDB.id == id)
        db_obj = self.session.exec(statement).first()
        if not db_obj:
            raise ValueError("User not found")
        return self._to_domain(db_obj)

    def get_all(self) -> List[UserDB]:
        statement = select(UserDB)
        rows = self.session.exec(statement).all()
        return [self._to_domain(row) for row in rows]

    def add(self, obj: UserDB) -> UserDB:
        return self.create_user(obj)

    def update(self, obj: UserDB) -> UserDB:
        statement = select(UserDB).where(UserDB.id == obj.id)
        db_obj = self.session.exec(statement).first()
        if not db_obj:
            raise ValueError("User not found")

        db_obj.username = obj.username
        db_obj.password_hash = obj.password_hash
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_domain(db_obj)

    def delete(self, id: int) -> None:
        statement = select(UserDB).where(UserDB.id == id)
        db_obj = self.session.exec(statement).first()
        if not db_obj:
            raise ValueError("User not found")

        self.session.delete(db_obj)
        self.session.commit()
    
    def create_user(self, data: UserDB) -> UserDB:
        db_obj = UserDB(
            username=data.username,
            password_hash=data.password_hash,
        )
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_domain(db_obj)

def get_user_repository(
    session: Session = Depends(get_session),
) -> UserRepository:
    return UserRepository(session=session)