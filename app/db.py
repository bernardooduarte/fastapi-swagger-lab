from typing import List

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models import Account, AccountCreate, AccountDB


def create_account_db(account_data: AccountCreate, session: Session) -> Account:
    account_db = AccountDB(
        owner=account_data.owner,
        type=account_data.type,
        balance=0.0,
    )
    session.add(account_db)
    session.commit()
    session.refresh(account_db)

    return Account(
        id=account_db.id,
        owner=account_db.owner,
        type=account_db.type,
        balance=account_db.balance,
    )


def get_account_by_id_db(account_id: int, session: Session) -> AccountDB:
    statement = select(AccountDB).where(AccountDB.id == account_id)
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail="Account not found")
    return result


def to_account_model(account_db: AccountDB) -> Account:
    return Account(
        id=account_db.id,
        owner=account_db.owner,
        type=account_db.type,
        balance=account_db.balance,
    )