from contracts import ERC721Contract
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


# Configuration
INFURA_URL = config('PROVIDER_URL')
ARTIST_PRIVATE_KEY = config('ARTIST_PRIVATE_KEY')
ARTIST_ADDRESS = config('ARTIST_ADDRESS')
YOUR_CHAIN_ID = config('CHAIN_ID')
YOUR_GAS_LIMIT = config('GAS_LIMIT')
CONTRACT_ADDRESS = config('MOCK_ERC721_CONTRACT_ADDRESS')

erc721Contract = ERC721Contract()  # Moved instantiation outside the loop

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
if w3.is_connected():
    print("Connected to Ethereum network!")
else:
    print("Not connected!")
    exit()

account = w3.eth.account.from_key(ARTIST_PRIVATE_KEY)


def main():
    print("Running")
    transaction = erc721Contract.set_approval_for_all()

    signed_txn = w3.eth.account.sign_transaction(
        transaction, ARTIST_PRIVATE_KEY)
    print("Signed txn: ", signed_txn)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transaction hash: {txn_hash.hex()}")


if __name__ == "__main__":
    main()
