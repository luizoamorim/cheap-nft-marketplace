import os
import sys
import time
from decouple import config
from web3 import Web3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from contracts import ERC721Contract

# Configuration
INFURA_URL = config('PROVIDER_URL')
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

erc721Contract = ERC721Contract()  # Moved instantiation outside the loop

if not w3.is_connected():
    print("Not connected to Ethereum network!")
    exit()


def listen_for_transfer_events():
    # Event signature for Transfer event
    transfer_event_signature = w3.keccak(
        text="Transfer(address,address,uint256)").hex()

    # Create a filter for catching Transfer events
    event_filter = w3.eth.filter({
        "fromBlock": "latest",
        "address": config('MOCK_ERC721_CONTRACT_ADDRESS'),
        "topics": [transfer_event_signature]
    })

    print("ERC721 listening...")

    contract_instance = erc721Contract.get_contract_instance()

    while True:
        events = event_filter.get_new_entries()
        for event in events:
            decoded_event = contract_instance.events.Transfer().process_log(event)
            print(decoded_event)

        # Use sleep to prevent spamming (you can adjust the sleep time as
        # desired)
        time.sleep(10)


if __name__ == "__main__":
    listen_for_transfer_events()
