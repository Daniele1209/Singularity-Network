from Exceptions import AccountModelError


class AccountModel:
    def __init__(self):
        self._accounts = []
        # map the public key to the amount of tokens
        # key: account public key
        # value: token count
        self._balances = {}

    def get_balance(self, account_publicKey):
        if account_publicKey not in self._accounts:
            self.add_account(account_publicKey)
        return self._balances[account_publicKey]

    def get_accounts(self):
        return self._accounts

    def add_account(self, account_publicKey):
        if account_publicKey not in self._accounts:
            self._accounts.append(account_publicKey)
            self._balances[account_publicKey] = 0

    def balance_update(self, account_publicKey, amount):
        if account_publicKey in self._accounts:
            self._balances[account_publicKey] += amount
        else:
            # raise AccountModelError("Account not found -update !")
            self._balances[account_publicKey] += amount
