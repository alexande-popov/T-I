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

    with AccountService() as service:
        # Получаем счета
        accounts = service.get_accounts()
        
        print("=" * 70)
        print("ИССЛЕДОВАНИЕ ПОРТФЕЛЯ")
        print("=" * 70)
        
        # Показываем все счета
        print("\n📁 ДОСТУПНЫЕ СЧЕТА:")
        for acc in accounts:
            acc_type = "Брокерский" if acc.type == 1 else "ИИС" if acc.type == 2 else "Инвесткопилка"
            print(f"   {acc.id[:8]}... - {acc.name} ({acc_type})")
        
        # Выбираем первый брокерский счет (не Инвесткопилку)
        brokerage = [acc for acc in accounts if acc.type != 3]
        if not brokerage:
            print("\n❌ Нет брокерских счетов")
            return
        
        account_id = brokerage[0].id
        print(f"\n✅ Анализируем счет: {brokerage[0].name} (ID: {account_id[:8]}...)")
        
        # Получаем портфель
        print("\n🔄 Получение данных портфеля...")
        portfolio = service.get_portfolio(account_id)
        
        print("\n" + "=" * 70)
        print("СТАТИСТИКА ПОРТФЕЛЯ")
        print("=" * 70)
        
        # Общая стоимость
        total = portfolio.total_amount_portfolio
        print(f"\n💰 ОБЩАЯ СТОИМОСТЬ:")
        print(f"   {total.units}.{total.nano:09d} {total.currency}")
        
        # Доходность
        yield_val = portfolio.expected_yield
        print(f"\n📈 ОЖИДАЕМАЯ ДОХОДНОСТЬ:")
        print(f"   {yield_val.units}.{yield_val.nano:09d} {total.currency}")
        
        # Количество позиций
        print(f"\n📊 ПОЗИЦИИ В ПОРТФЕЛЕ: {len(portfolio.positions)}")
        
        if len(portfolio.positions) == 0:
            print("   Портфель пуст")
            return
        
        print("\n" + "-" * 70)
        
        # Выводим каждую позицию
        for i, pos in enumerate(portfolio.positions, 1):
            print(f"\n{i}. ИНСТРУМЕНТ:")
            print(f"   FIGI: {pos.figi}")
            print(f"   Тип: {pos.instrument_type}")
            
            # Количество
            qty = pos.quantity
            print(f"\n   КОЛИЧЕСТВО:")
            print(f"     {qty.units}.{qty.nano:09d} шт.")
            
            # Текущая цена
            price = pos.current_price
            print(f"\n   ТЕКУЩАЯ ЦЕНА:")
            print(f"     {price.units}.{price.nano:09d} {price.currency}")
            
            # Средняя цена покупки
            avg_price = pos.average_position_price
            print(f"\n   СРЕДНЯЯ ЦЕНА ПОКУПКИ:")
            print(f"     {avg_price.units}.{avg_price.nano:09d} {avg_price.currency}")
            
            # Доходность позиции (без валюты)
            if hasattr(pos, 'expected_yield'):
                pos_yield = pos.expected_yield
                print(f"\n   ДОХОДНОСТЬ ПОЗИЦИИ:")
                print(f"     {pos_yield.units}.{pos_yield.nano:09d} {total.currency}")
            
            # Доходность позиции
            # pos_yield = pos.expected_yield
            # print(f"\n   ДОХОДНОСТЬ ПОЗИЦИИ:")
            # print(f"     {pos_yield.units}.{pos_yield.nano:09d} {pos_yield.currency}")
            
            # Заблокировано?
            if pos.blocked:
                print(f"\n   ⚠️ ЗАБЛОКИРОВАНО ДЕПОЗИТАРИЕМ")
            
            print("-" * 50)
        
        # Дополнительная информация
        print("\n" + "=" * 70)
        print("ДОПОЛНИТЕЛЬНЫЕ ДАННЫЕ")
        print("=" * 70)
        
        # Есть ли валютные позиции?
        if hasattr(portfolio, 'total_amount_currencies'):
            currencies = portfolio.total_amount_currencies
            print(f"\n💱 ВАЛЮТНЫЕ ПОЗИЦИИ:")
            print(f"   {currencies.units}.{currencies.nano:09d} {currencies.currency}")
        
        # Заблокированы ли активы?
        if hasattr(portfolio, 'blocked'):
            print(f"\n🔒 БЛОКИРОВКА АКТИВОВ:")
            print(f"   {'Да' if portfolio.blocked else 'Нет'}")
        
        # Выводим все поля portfolio (для исследования)
        print("\n" + "=" * 70)
        print("ВСЕ ПОЛЯ ОБЪЕКТА PORTFOLIO")
        print("=" * 70)
        for attr in dir(portfolio):
            if not attr.startswith('_') and not callable(getattr(portfolio, attr)):
                print(f"   {attr}")

if __name__ == "__main__":
    main()
