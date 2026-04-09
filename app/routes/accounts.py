from fastapi import APIRouter, HTTPException, Depends

from app.auth import get_current_user
from app.schemas.account_schemas import AccountCreate, AccountResponse
from app.models import Amount
from app.controllers.accounts import AccountController, get_account_controller

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=AccountResponse)
def create_account(
    account_data: AccountCreate,
    controller: AccountController = Depends(get_account_controller),
    user: dict = Depends(get_current_user),
):
    return controller.create_from_input(account_data)


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    controller: AccountController = Depends(get_account_controller),
    user: dict = Depends(get_current_user),
):
    try:
        return controller.get(account_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Account not found")


@router.post("/{account_id}/deposit", response_model=AccountResponse)
def deposit(
    account_id: int,
    amount: Amount,
    controller: AccountController = Depends(get_account_controller),
    user: dict = Depends(get_current_user),
):
    if amount.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    try:
        return controller.deposit(account_id, amount.amount)
    except ValueError as e:
        msg = str(e)
        if msg == "Account not found":
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)


@router.post("/{account_id}/withdraw", response_model=AccountResponse)
def withdraw(
    account_id: int,
    amount: Amount,
    controller: AccountController = Depends(get_account_controller),
    user: dict = Depends(get_current_user),
):
    if amount.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    try:
        return controller.withdraw(account_id, amount.amount)
    except ValueError as e:
        msg = str(e)
        if msg == "Account not found":
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)