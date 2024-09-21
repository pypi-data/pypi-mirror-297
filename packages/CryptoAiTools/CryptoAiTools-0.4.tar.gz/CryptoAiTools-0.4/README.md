
# Crypto DEX Bot Creator

This Python module enables the creation of automated trading bots that operate on decentralized exchanges (DEXs). It interacts with DEXs using the `web3.py` library and smart contracts to execute token swaps and manage liquidity.

## Features:
- Automatically swap tokens based on price thresholds.
- Monitors token prices and executes trades in real-time.
- Adds or removes liquidity from DEX pools based on user-defined limits.
- Compatible with Ethereum, Binance Smart Chain (BSC), and other EVM-based networks.
- Simulated RPC server for testing and future integrations.
- Multi-threaded to allow real-time operations like price monitoring and liquidity management simultaneously.

## Requirements:
- Python 3.x
- `web3.py` and `Solana` library
- An Ethereum-compatible wallet (e.g., MetaMask, TrustWallet)
- Smart contract ABI file (`abi.json`)
- RPC URL for the blockchain network (e.g., BSC, Ethereum Mainnet)

## Installation:
Clone the repository and install the required dependencies using `pip`.

```bash
git clone https://github.com/CryptoAiBotCreator/CryptoAi-Bot-Creator
cd CryptoAi-Bot-Creator
pip install -r requirements.txt
python3 
```

## Usage:
Initialize the bot by passing the necessary parameters such as the DEX contract address, wallet details, and RPC URL.

```python
from crypto_bot_creator.bot_creator import DEXBot

# Example usage
bot = DEXBot(
    'MyDEXBot', 
    'dex_contract_address', 
    'wallet_address', 
    'private_key', 
    'https://rpc_url', 
    'token_in_address', 
    'token_out_address'
)

# Start trading based on price monitoring
bot.run()
```

## License:
This project is licensed under the MIT License. See the LICENSE file for more details.

