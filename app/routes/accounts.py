from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from app.auth import get_current_user
from app.database import get_session
from app.db import create_account_db, get_account_by_id_db, to_account_model
from app.models import Account, AccountCreate, Amount

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=Account)
def create_account(
    account_data: AccountCreate,
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    return create_account_db(account_data, session)


@router.get("/{account_id}", response_model=Account)
def get_account(
    account_id: int,
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    account_db = get_account_by_id_db(account_id, session)
    return to_account_model(account_db)


@router.post("/{account_id}/deposit", response_model=Account)
def deposit(
    account_id: int,
    amount: Amount,
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    account_db = get_account_by_id_db(account_id, session)
    account_db.balance += amount.amount
    session.add(account_db)
    session.commit()
    session.refresh(account_db)
    return to_account_model(account_db)


@router.post("/{account_id}/withdraw", response_model=Account)
def withdraw(
    account_id: int,
    amount: Amount,
    session: Session = Depends(get_session),
    user: dict = Depends(get_current_user),
):
    account_db = get_account_by_id_db(account_id, session)

    if amount.amount > account_db.balance:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    account_db.balance -= amount.amount
    session.add(account_db)
    session.commit()
    session.refresh(account_db)
    return to_account_model(account_db)