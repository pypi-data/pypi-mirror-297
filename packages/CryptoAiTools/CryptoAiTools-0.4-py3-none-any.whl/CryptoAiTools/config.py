class Config:
    def __init__(self, rpc_url, wallet_address, private_key):
        self.rpc_url = rpc_url
        self.wallet_address = wallet_address
        self.private_key = private_key

    def get_rpc_url(self):
        return self.rpc_url

    def get_wallet_address(self):
        return self.wallet_address

    def get_private_key(self):
        return self.private_key
