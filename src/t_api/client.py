from t_tech.invest import Client
from src.config import TOKEN
from src.models.account import Account

class TInvestAPI:
    """Клиент для работы с T-Invest API"""
    
    def __init__(self, token=None):
        self.token = token or TOKEN
        self._raw_client = None  # исходный Client (имеет __exit__)
        self._services = None    # Services объект (имеет users, operations)
        self._init_client()
    
    def _init_client(self):
        """Инициализация клиента и сервисов"""
        self._raw_client = Client(self.token)
        self._services = self._raw_client.__enter__()
    
    def close(self):
        """Закрывает клиент"""
        if self._raw_client:
            self._raw_client.__exit__(None, None, None)
            self._raw_client = None
            self._services = None
    
    @property
    def client(self):
        if self._services is None:
            self._init_client()
        return self._services
    
    def get_accounts(self):
        """Получить список счетов"""
        response = self.client.users.get_accounts()
        return [Account(acc) for acc in response.accounts]
    
    def get_portfolio(self, account_id):
        """Получить портфель по ID счета"""
        return self.client.operations.get_portfolio(account_id=account_id)
    
    def get_instrument_by_figi(self, figi):
        """Получить инструмент по FIGI"""
        return self.client.instruments.get_instrument_by(figi=figi)