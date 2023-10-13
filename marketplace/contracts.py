"""
Module for handling contracts interaction in the marketplace.
"""
import json
import os
from decouple import config
from web3 import Web3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ERC721Contract:
    """
    A class to interact with the ERC721 smart contract on the Ethereum blockchain.

    Attributes:
        PROVIDER_URL (str): The Ethereum network provider's URL.
        MOCK_ERC721_CONTRACT_ADDRESS (str): The Ethereum address of the MOCK ERC721 contract.
        ERC721_ABI_PATH (str): Path to the ABI (Application Binary Interface) of
        the ERC721 contract.
        MOCK_ERC721_ABI (list): Loaded ABI content from the JSON file.
    """

    PROVIDER_URL = config('PROVIDER_URL')
    MOCK_ERC721_CONTRACT_ADDRESS = config('MOCK_ERC721_CONTRACT_ADDRESS')
    ERC721_ABI_PATH = os.path.join(
        BASE_DIR, 'contractsABI', 'MOCK_ERC721.json')

    with open(ERC721_ABI_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        MOCK_ERC721_ABI = json.loads(data['result'])

    def __init__(self):
        """
        Initialize an instance of the ERC721Contract class.
        Sets up the web3 instance and the contract.
        """
        self.contract_address = self.MOCK_ERC721_CONTRACT_ADDRESS
        self.w3 = Web3(Web3.HTTPProvider(self.PROVIDER_URL))
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.MOCK_ERC721_ABI
        )

    def get_owner_of_token(self, token_id):
        """
        Initialize an instance of the ERC721Contract class.
        Sets up the web3 instance and the contract.
        """
        return self.contract.functions.ownerOf(token_id).call()

    def is_token_owner(self, address, token_id):
        """
        Check if the given address is the owner of the specified token ID.

        Args:
            address (str): Ethereum address to check.
            token_id (int): The ID of the token.

        Returns:
            bool: True if the provided address is the owner, False otherwise.
        """
        return self.get_owner_of_token(token_id) == address


class MarketplaceContract:
    PROVIDER_URL = config('PROVIDER_URL')
    MARKETPLACE_ADDRESS = config('MARKETPLACE_ADDRESS')
    MARKETPLACE_ABI_PATH = os.path.join(
        BASE_DIR, 'contractsABI', 'MARKETPLACE.json')

    with open(MARKETPLACE_ABI_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        MARKETPLACE_ABI = json.loads(data['result'])

    def __init__(self):
        """
        Initialize an instance of the ERC721Contract class.
        Sets up the web3 instance and the contract.
        """
        self.contract_address = self.MARKETPLACE_ADDRESS
        self.w3 = Web3(Web3.HTTPProvider(self.PROVIDER_URL))
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.MARKETPLACE_ABI
        )

    def send_transaction(
            self,
            nft_collection_address,
            token_id,
            erc20_address,
            erc20_amount,
            bidder_sig,
            owner_approval_sig,
            owner_address):

        # Construct the auction data
        auction_data = {
            "collectionAddress": nft_collection_address,
            "erc20Address": erc20_address,
            "tokenId": token_id,
            "bid": erc20_amount
        }

        # Send the transaction
        txn = self.contract.functions.finishAuction(
            auction_data,
            bidder_sig,
            owner_approval_sig
        ).build_transaction({
            'chainId': config("CHAIN_ID"),
            'gas': config("GAS_LIMIT"),
            'gasPrice': self.w3.to_wei('20', 'gwei'),
            'nonce': self.w3.eth.get_transaction_count(owner_address)
        })

        return txn
