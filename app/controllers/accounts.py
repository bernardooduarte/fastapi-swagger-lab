from fastapi import Depends

from app.controllers.base import Controller
from app.models import Account, AccountCreate
from app.repositories.accounts import AccountRepository, get_account_repository


class AccountController(Controller[Account]):
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def get(self, id: int) -> Account:
        return self.repository.get(id)

    def get_all(self):
        return self.repository.get_all()

    def add(self, obj: Account) -> Account:
        return self.repository.add(obj)

    def update(self, obj: Account) -> Account:
        return self.repository.update(obj)

    def delete(self, id: int) -> None:
        self.repository.delete(id)

    def create_from_input(self, data: AccountCreate) -> Account:
        return self.repository.create_from_input(data)

    def deposit(self, account_id: int, amount: float) -> Account:
        account = self.repository.get(account_id)
        account.balance += amount
        return self.repository.update(account)

    def withdraw(self, account_id: int, amount: float) -> Account:
        account = self.repository.get(account_id)

        if amount > account.balance:
            raise ValueError("Insufficient funds")

        account.balance -= amount
        return self.repository.update(account)


def get_account_controller(
    repository: AccountRepository = Depends(get_account_repository),
) -> AccountController:
    return AccountController(repository=repository)