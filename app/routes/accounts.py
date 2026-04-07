from fastapi import APIRouter, HTTPException, Depends

from app.auth import get_current_user
from app.models import Account, AccountCreate, Amount
from app.repositories.accounts import AccountRepository, get_account_repository

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=Account)
def create_account(
    account_data: AccountCreate,
    repo: AccountRepository = Depends(get_account_repository),
    user: dict = Depends(get_current_user),
):
    return repo.create_from_input(account_data)


@router.get("/{account_id}", response_model=Account)
def get_account(
    account_id: int,
    repo: AccountRepository = Depends(get_account_repository),
    user: dict = Depends(get_current_user),
):
    try:
        return repo.get(account_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Account not found")


@router.post("/{account_id}/deposit", response_model=Account)
def deposit(
    account_id: int,
    amount: Amount,
    repo: AccountRepository = Depends(get_account_repository),
    user: dict = Depends(get_current_user),
):
     try:
        return repo.deposit(account_id, amount.amount)
     except ValueError as e:
         msg = str(e)
         if msg == "Account not found":
            raise HTTPException(status_code=404, detail=msg)
         raise HTTPException(status_code=400, detail=msg)


@router.post("/{account_id}/withdraw", response_model=Account)
def withdraw(
    account_id: int,
    amount: Amount,
    repo: AccountRepository = Depends(get_account_repository),
    user: dict = Depends(get_current_user),
):
    try:
        return repo.withdraw(account_id, amount.amount)
    except ValueError as e:
         msg = str(e)
         if msg == "Account not found":
            raise HTTPException(status_code=404, detail=msg)
         raise HTTPException(status_code=400, detail=msg)