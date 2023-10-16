import requests
import json
from decouple import config
from web3 import Web3
from eth_account.messages import encode_defunct

INFURA_URL = config('PROVIDER_URL')
ARTIST_PRIVATE_KEY = config('ARTIST_PRIVATE_KEY')
ARTIST_ADDRESS = config('ARTIST_ADDRESS')
COLLECTOR_PRIVATE_KEY = config('COLLECTOR_PRIVATE_KEY')
COLLECTOR_ADDRESS = config('COLLECTOR_ADDRESS')
YOUR_CHAIN_ID = config('CHAIN_ID')
YOUR_GAS_LIMIT = config('GAS_LIMIT')
MOCK_ERC721_CONTRACT_ADDRESS = config('MOCK_ERC721_CONTRACT_ADDRESS')
MOCK_ERC20_CONTRACT_ADDRESS = config('MOCK_ERC20_CONTRACT_ADDRESS')
BASE_URL = config('BASE_URL')
TOKEN_ID = config('TOKEN_ID')

w3 = Web3(Web3.HTTPProvider(INFURA_URL))


def list_nft(data):
    response = requests.post(f"{BASE_URL}/list/", json=data)
    return response.json()


def purchase_nft(data):
    # Create a message to be signed
    message = w3.solidity_keccak(
        ['address', 'address', 'uint256', 'uint256'],
        [data.get('nft_collection_address'),
         data.get('erc20Address'),
         int(data.get('tokenId')),
         int(data.get('erc20_amount'))]
    )

    # Sign the message
    signable_message = encode_defunct(hexstr=message.hex())
    signature = w3.eth.account.sign_message(
        signable_message, private_key=COLLECTOR_PRIVATE_KEY)

    # Update the data with signature and buyer address
    data.update({'bidderSig': signature.signature.hex()})
    data.update({'buyerAddress': COLLECTOR_ADDRESS})

    # Print the updated data (For debugging purposes, can be removed later)
    print("Data to be sent for purchase:", data)
    response = requests.post(f"{BASE_URL}/purchaseOrder/", json=data)
    print(f"Purchase Response: {response.json()}")
    return data


def settle_purchase_order(sale_id, collector_signature):

    buyer_signature_hash = w3.solidity_keccak(['bytes'], [collector_signature])

    # Encode the hash for signing
    signable_buyer_signature_hash = encode_defunct(
        hexstr=buyer_signature_hash.hex())

    # Artist signs the hash of buyer's signature using their private key
    artist_signature = w3.eth.account.sign_message(
        signable_buyer_signature_hash, private_key=ARTIST_PRIVATE_KEY)

    body_data = {
        "sale_id": sale_id,  # This might be dynamic, so you can adjust accordingly
        "owner_approval_sig": artist_signature.signature.hex(),
        "owner_address": ARTIST_ADDRESS
    }
    response = requests.post(
        f"{BASE_URL}/settle_purchase_order/",
        json=body_data)
    return response.json()


if __name__ == "__main__":
    # Listing an NFT
    list_data = {
        "nft_collection_address": MOCK_ERC721_CONTRACT_ADDRESS,
        "tokenId": int(TOKEN_ID),
        "erc20Address": MOCK_ERC20_CONTRACT_ADDRESS,
        "erc20_amount": 10500000000000000,
        "isAuction": False,
        "ownerAddress": ARTIST_ADDRESS
    }

    list_response = list_nft(list_data)
    print(f"Listing Response: {list_response}")

    sale_id = list_response.get("sale_id")

    if sale_id:
        # Purchasing the listed NFT
        purchase_data = {
            "nft_collection_address": MOCK_ERC721_CONTRACT_ADDRESS,
            "tokenId": TOKEN_ID,
            "erc20Address": MOCK_ERC20_CONTRACT_ADDRESS,
            "erc20_amount": 10500000000000000,
            "bidderSig": "",
            "buyerAddress": "",
            "sale_id": sale_id
        }

        purchase_response = purchase_nft(purchase_data)

        settle_response = settle_purchase_order(
            sale_id, purchase_response.get("bidderSig"))
        print(f"Settle Response: {settle_response}")

        # Extract the transaction from the response
        unsigned_transaction = settle_response['txHash']
        unsigned_transaction['chainId'] = int(unsigned_transaction['chainId'])

        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(
            unsigned_transaction, ARTIST_PRIVATE_KEY)
        print("Signed txn: ", signed_txn)

        # Send the signed transaction
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"Transaction hash: {txn_hash.hex()}")
    else:
        print("Failed to list the NFT. Exiting the script.")
