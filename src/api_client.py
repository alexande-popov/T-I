from t_tech.invest import Client
from src.config import TOKEN

class TInvestAPI:
    """Клиент для работы с T-Invest API"""
    
    def __init__(self, token=None):
        self.token = token or TOKEN
        self._client = None
    
    @property
    def client(self):
        """Ленивая инициализация клиента"""
        if self._client is None:
            self._client = Client(self.token)
        return self._client