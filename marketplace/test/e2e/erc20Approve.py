from web3 import Web3
from decouple import config
import json
import os
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from contracts import ERC20Contract

# Configuration
INFURA_URL = config('PROVIDER_URL')
COLLECTOR_PRIVATE_KEY = config('COLLECTOR_PRIVATE_KEY')
COLLECTOR_ADDRESS = config('COLLECTOR_ADDRESS')
YOUR_CHAIN_ID = config('CHAIN_ID')
YOUR_GAS_LIMIT = config('GAS_LIMIT')
CONTRACT_ADDRESS = config('MOCK_ERC20_CONTRACT_ADDRESS')
MARKETPLACE_CONTRACT_ADDRESS = config('MARKETPLACE_ADDRESS')

erc20Contract = ERC20Contract()  # Moved instantiation outside the loop

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
if w3.is_connected():
    print("Connected to Ethereum network!")
else:
    print("Not connected!")
    exit()

account = w3.eth.account.from_key(COLLECTOR_PRIVATE_KEY)


def main():
    print("Running")
    transaction = erc20Contract.approve(
        MARKETPLACE_CONTRACT_ADDRESS, 10500000000000000)

    signed_txn = w3.eth.account.sign_transaction(
        transaction, COLLECTOR_PRIVATE_KEY)
    print("Signed txn: ", signed_txn)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transaction hash: {txn_hash.hex()}")


if __name__ == "__main__":
    main()
