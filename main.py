import os
from dotenv import load_dotenv
from t_tech.invest import Client


load_dotenv()
TOKEN = os.getenv("TINKOFF_TOKEN_ONLY_READ")

def main():
    # Создаем клиента с токеном
    with Client(TOKEN) as client:
        # Пример 1: Получить информацию о счетах
        accounts = client.users.get_accounts()
        for account in accounts.accounts:
            print(f"Счет: {account.id}, Статус: {account.status}")

if __name__ == "__main__":
    main()
