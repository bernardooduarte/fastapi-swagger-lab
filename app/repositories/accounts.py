from typing import List

from sqlmodel import Session, select
from fastapi import Depends

from app.repositories.base import Repository
from app.models import Account, AccountDB, AccountCreate
from app.db import get_account_by_id_db
from app.database import get_session

class AccountRepository(Repository[Account]):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, db_obj: AccountDB) -> Account:
        return Account(
            id=db_obj.id,
            owner=db_obj.owner,
            type=db_obj.type,
            balance=db_obj.balance,
        )
    
    def get(self, id: int) -> Account:
        statement = select(AccountDB).where(AccountDB.id == id)
        db_obj = self.session.exec(statement).first()
        if not db_obj:
            raise ValueError("Account not found")
        return self._to_domain(db_obj)
    
    def get_all(self) -> List[Account]:
        statement = select(AccountDB)
        results = self.session.exec(statement).all()
        return [self._to_domain(row) for row in results]
    
    def add(self, obj: Account) -> Account:
        db_obj = AccountDB(
            owner=obj.owner,
            type=obj.type,
            balance=obj.balance,
        )
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_domain(db_obj)
    
    def update(self, obj: Account) -> Account:
        statement = select(AccountDB).where(AccountDB.id == obj.id)
        db_obj = self.session.exec(statement).first()
        if not db_obj:
            raise ValueError("Account not found")
        
        db_obj.owner = obj.owner
        db_obj.type = obj.type
        db_obj.balance = obj.balance

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_domain(db_obj)
    
    def delete(self, id: int) -> None:
        statement = select(AccountDB).where(AccountDB.id == id)
        db_obj = self.session.exec(statement).first()
        if not db_obj:
            raise ValueError("Account not found")
        
        self.session.delete(db_obj)
        self.session.commit()

    def create_from_input(self, data: AccountCreate) -> Account:

        db_obj=AccountDB(
            owner=data.owner,
            type=data.type,
            balance=0.0
        )
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_domain(db_obj)
    
    
    def deposit(self, account_id: int, amount: float) -> Account:
        statement = select(AccountDB).where(AccountDB.id == account_id)
        db_obj = self.session.exec(statement).first()
        if not db_obj:
            raise ValueError("Account not found")

        db_obj.balance += amount
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_domain(db_obj)
    
    def withdraw(self, account_id: int, amount: float) -> Account:
        statement = select(AccountDB).where(AccountDB.id == account_id)
        db_obj = self.session.exec(statement).first()
        if not db_obj:
            raise ValueError("Account not found")

        if amount > db_obj.balance:
            raise ValueError("Insufficient funds")

        db_obj.balance -= amount
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_domain(db_obj)
    
def get_account_repository(
        session: Session = Depends(get_session),
) -> AccountRepository:
    return AccountRepository(session=session)