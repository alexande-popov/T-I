from src.t_api.client import TInvestAPI
from src.models.account import AccountStorage

class AccountService:
    """Сервис для работы с аккаунтами (бизнес-логика)"""
    def __init__(self):
        self._api = None
        self._storage = AccountStorage()
    
    def __enter__(self):
        self._api = TInvestAPI()
        self._sync_accounts()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._api:
            self._api.close()
    
    def _sync_accounts(self):
        accounts = self._api.get_accounts()
        for account in accounts:
            self._storage.add_account(account)
    
    def get_accounts(self):
        return self._storage.get_accounts()
    
    def get_portfolio(self, account_id):
        """Возвращает портфель по ID счета"""
        return self._api.get_portfolio(account_id)
