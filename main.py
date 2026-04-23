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
            print(f"\nСчет: {account.id}, Статус: {account.status}")

            if hasattr(account, '__dict__'):
                for key, value in account.__dict__.items():
                    print(f"  {key}: {value}")


        # Выбираем счет (например, первый обычный брокерский)
        account_id = None
        for account in accounts.accounts:
            if account.type != 3:  # 3 = INVEST_BOX (Инвесткопилка)
                account_id = account.id
                break
        
        if not account_id:
            print("Нет доступных счетов для анализа портфеля")
            return
        
        # Получаем портфель
        portfolio = client.operations.get_portfolio(account_id=account_id)
        
        print("=" * 60)
        print("СТАТИСТИКА ПОРТФЕЛЯ")
        print("=" * 60)
        
        # Общая стоимость
        total = portfolio.total_amount_portfolio
        print(f"💰 Общая стоимость: {total.units}.{total.nano:09d} {total.currency}")
        
        # Доходность (Quotation - только число, без валюты)
        yield_val = portfolio.expected_yield
        print(f"📈 Ожидаемая доходность: {yield_val.units}.{yield_val.nano:09d} руб.")
        
        print(f"\n📊 ПОЗИЦИИ В ПОРТФЕЛЕ:")
        print("-" * 60)
        
        for position in portfolio.positions:
            # Получаем название инструмента по FIGI
            try:
                instrument = client.instruments.get_instrument_by(figi=position.figi)
                name = instrument.name
            except:
                name = position.figi  # Если не удалось получить имя, используем FIGI
            
            # Количество в штуках
            quantity = position.quantity
            qty_str = f"{quantity.units}.{quantity.nano:09d}"
            
            # Текущая цена
            price = position.current_price
            price_str = f"{price.units}.{price.nano:09d} {price.currency}"
            
            print(f"  • {name}")
            print(f"    FIGI: {position.figi}")
            print(f"    Тип: {position.instrument_type}")
            print(f"    Количество: {qty_str} шт.")
            print(f"    Текущая цена: {price_str}")
            print()


if __name__ == "__main__":
    main()
