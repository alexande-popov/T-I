import json


class Account:
    """Аккаунт, динамически созданный из API объекта"""
    
    def __init__(self, api_account):
        for attr in dir(api_account):
            # Берём только не-методы и не служебные
            if not attr.startswith('_') and not callable(getattr(api_account, attr)):
                setattr(self, attr, getattr(api_account, attr))
    
    def __repr__(self):
        return f"Account(id={self.id}, name={self.name})"
    
    def to_dict(self):
        """Экспорт в словарь"""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}


class AccountStorage:
    """Список аккаунтов"""

    def __init__(self, accounts=None):
        self._accounts = accounts if accounts else []

    def add_account(self, account: Account):
        self._accounts.append(account)

    def remove_account(self, account_id):
        self._accounts.remove(account_id)

    def get_accounts(self):
        return self._accounts
    
    def save_to_json(self, path="data/accounts.json"):
        data = [acc.to_dict() for acc in self._accounts]
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, default=str)