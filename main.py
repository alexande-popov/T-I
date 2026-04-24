from t_tech.invest import Client

from src.config import TOKEN
from src.models.account import Account, AccountStorage

def main():
    # Создаем клиента с токеном
    with Client(TOKEN) as client:
        # Пример 1: Получить информацию о счетах
        accounts_response = client.users.get_accounts()

        storage = AccountStorage()

        for api_account in accounts_response.accounts:
            account = Account(api_account)
            storage.add_account(account)
            print(f"Добавлен: {account.name} ({account.id})")

    for account in storage.get_accounts():
        print(f"\nСчет: {account.id}, Статус: {account.status}")

        if hasattr(account, '__dict__'):
            for key, value in account.__dict__.items():
                print(f"  {key}: {value}")

    # ИЛИ лучще через контроллер
    from src.services.account_service import AccountService

    with AccountService() as service:
        accounts = service.get_accounts()
        for account in accounts:
            print(f"{account.name} ({account.id})")


if __name__ == "__main__":
    main()
