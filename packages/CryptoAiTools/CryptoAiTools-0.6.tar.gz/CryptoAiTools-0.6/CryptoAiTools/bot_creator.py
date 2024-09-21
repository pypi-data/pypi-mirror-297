from web3 import Web3
import json
import logging
import time
import random
from threading import Thread
from queue import Queue

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DEXBot:
    def __init__(self, name, dex_contract_address, wallet_address, private_key, rpc_url, token_in, token_out, slippage=0.01):
        self.name = name
        self.dex_contract_address = dex_contract_address
        self.wallet_address = wallet_address
        self.private_key = private_key
        self.rpc_url = rpc_url
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        self.dex_contract = self.load_dex_contract()
        self.token_in = token_in
        self.token_out = token_out
        self.slippage = slippage
        self.data_queue = Queue()

    def load_dex_contract(self):
        """Load DEX smart contract ABI"""
        with open('abi.json', 'r') as abi_file:
            abi = json.load(abi_file)
        contract = self.web3.eth.contract(address=self.dex_contract_address, abi=abi)
        return contract

    def check_balance(self, token_address):
        """Check token balance in the wallet"""
        token_contract = self.web3.eth.contract(address=token_address, abi=self.dex_contract.abi)
        balance = token_contract.functions.balanceOf(self.wallet_address).call()
        logging.info(f"Balance of token {token_address}: {balance}")
        return balance

    def estimate_gas(self, amount_in, token_in, token_out):
        """Estimate gas cost for swap"""
        gas_estimate = self.dex_contract.functions.swapExactTokensForTokens(
            amount_in,
            0,  # Slippage and minimum output handled later
            [token_in, token_out],
            self.wallet_address,
            int(time.time()) + 1000
        ).estimateGas({'from': self.wallet_address})
        logging.info(f"Estimated gas for swap: {gas_estimate}")
        return gas_estimate

    def get_token_price(self, amount_in, token_in, token_out):
        """Fetch price of tokens in the DEX pool"""
        amounts_out = self.dex_contract.functions.getAmountsOut(amount_in, [token_in, token_out]).call()
        price = amounts_out[-1]
        logging.info(f"Price for {amount_in} {token_in}: {price} {token_out}")
        return price

    def swap_tokens(self, amount_in, token_in, token_out):
        """Execute token swap"""
        nonce = self.web3.eth.getTransactionCount(self.wallet_address)
        gas_estimate = self.estimate_gas(amount_in, token_in, token_out)
        min_amount_out = int(self.get_token_price(amount_in, token_in, token_out) * (1 - self.slippage))
        
        swap_txn = self.dex_contract.functions.swapExactTokensForTokens(
            amount_in,
            min_amount_out,  # Minimum amount out (with slippage)
            [token_in, token_out],
            self.wallet_address,
            int(time.time()) + 1000
        ).buildTransaction({
            'from': self.wallet_address,
            'gas': gas_estimate,
            'gasPrice': self.web3.toWei('5', 'gwei'),
            'nonce': nonce,
        })

        signed_txn = self.web3.eth.account.sign_transaction(swap_txn, private_key=self.private_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        logging.info(f"Swap transaction sent! Tx hash: {self.web3.toHex(tx_hash)}")
        return self.web3.toHex(tx_hash)

    def monitor_price_and_trade(self, amount_in, token_in, token_out, threshold_price):
        """Monitor token price and execute trade if conditions are met"""
        while True:
            current_price = self.get_token_price(amount_in, token_in, token_out)
            if current_price >= threshold_price:
                logging.info(f"Threshold met: executing trade. Current price: {current_price}, Target: {threshold_price}")
                self.swap_tokens(amount_in, token_in, token_out)
                break
            else:
                logging.info(f"Price below threshold. Current: {current_price}, Target: {threshold_price}")
            time.sleep(random.randint(1, 5))

    def start_price_monitoring(self, amount_in, token_in, token_out, threshold_price):
        """Start monitoring price in a separate thread"""
        price_monitor_thread = Thread(target=self.monitor_price_and_trade, args=(amount_in, token_in, token_out, threshold_price))
        price_monitor_thread.start()

    def rpc_server(self):
        """Simulate an RPC server for bot communication"""
        while True:
            block = {
                'block_number': random.randint(1, 10000),
                'transactions': [f'tx_{random.randint(1000, 9999)}' for _ in range(random.randint(1, 10))],
                'timestamp': time.time()
            }
            json_data = json.dumps(block)
            self.data_queue.put(json_data)
            logging.info(f"RPC Server: Generated block {block['block_number']}")
            time.sleep(random.randint(1, 3))

    def start_rpc_server(self):
        """Start RPC server in a separate thread"""
        rpc_server_thread = Thread(target=self.rpc_server)
        rpc_server_thread.start()

    def automatic_liquidity_management(self, min_liquidity, max_liquidity, token_address):
        """Monitor and manage liquidity in the DEX pool"""
        while True:
            pool_liquidity = self.check_liquidity(token_address)
            if pool_liquidity < min_liquidity:
                logging.info(f"Liquidity below minimum. Adding liquidity... Pool: {pool_liquidity}, Min: {min_liquidity}")
                self.add_liquidity(token_address, min_liquidity)
            elif pool_liquidity > max_liquidity:
                logging.info(f"Liquidity above maximum. Removing liquidity... Pool: {pool_liquidity}, Max: {max_liquidity}")
                self.remove_liquidity(token_address, max_liquidity)
            else:
                logging.info(f"Liquidity within acceptable range. Pool: {pool_liquidity}")
            time.sleep(random.randint(10, 20))

    def check_liquidity(self, token_address):
        """Check current liquidity in the pool for a given token"""
        # Mocked liquidity check
        liquidity = random.randint(1000, 10000)
        logging.info(f"Checked liquidity for token {token_address}: {liquidity}")
        return liquidity

    def add_liquidity(self, token_address, amount):
        """Add liquidity to the DEX pool"""
        logging.info(f"Adding {amount} liquidity to pool for token {token_address}")
        # Implement actual DEX liquidity addition here

    def remove_liquidity(self, token_address, amount):
        """Remove liquidity from the DEX pool"""
        logging.info(f"Removing {amount} liquidity from pool for token {token_address}")
        # Implement actual DEX liquidity removal here

    def run(self):
        """Main execution of the bot"""
        logging.info(f"{self.name} bot is running...")
        self.start_rpc_server()
        self.start_price_monitoring(100, self.token_in, self.token_out, 2000)
        self.automatic_liquidity_management(5000, 8000, self.token_in)
