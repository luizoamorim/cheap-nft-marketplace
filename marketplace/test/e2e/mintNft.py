import json
import sys
sys.path.append('../../') 

from decouple import config
from web3 import Web3
import contracts


# Configuration
INFURA_URL = 'YOUR_INFURA_URL'
PRIVATE_KEY = 'YOUR_PRIVATE_KEY'
YOUR_CHAIN_ID = 4  # for Rinkeby testnet
YOUR_GAS_LIMIT = 21000  # modify based on your contract's requirements
CONTRACT_ADDRESS = 'YOUR_CONTRACT_ADDRESS'
with open('path_to_your_ABI.json', 'r') as f:
    ABI = json.load(f)

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
if w3.isConnected():
    print("Connected to Ethereum network!")
else:
    print("Not connected!")
    exit()

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
account = w3.eth.account.privateKeyToAccount(PRIVATE_KEY)

def main():
    owner_address = input("Enter the address to mint the token to: ")
    transaction = contracts.mint_erc721_transaction(owner_address)
    
    signed_txn = w3.eth.account.signTransaction(transaction, PRIVATE_KEY)
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(f"Transaction hash: {txn_hash.hex()}")

if __name__ == "__main__":
    main()