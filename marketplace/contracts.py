"""
Module for handling contracts interaction in the marketplace.
"""
import json
import os
from decouple import config
from web3 import Web3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ERC20Contract:
    """
    A class to interact with the ERC20 smart contract on the Ethereum blockchain.

    Attributes:
        PROVIDER_URL (str): The Ethereum network provider's URL.
        MOCK_ERC20_CONTRACT_ADDRESS (str): The Ethereum address of the MOCK ERC20 contract.
        ERC20_ABI_PATH (str): Path to the ABI (Application Binary Interface) of
        the ERC20 contract.
        MOCK_ERC20_ABI (list): Loaded ABI content from the JSON file.
    """

    PROVIDER_URL = config('PROVIDER_URL')
    MOCK_ERC20_CONTRACT_ADDRESS = config('MOCK_ERC20_CONTRACT_ADDRESS')
    ERC20_ABI_PATH = os.path.join(
        BASE_DIR, 'contractsABI', 'MOCK_ERC20.json')

    with open(ERC20_ABI_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        MOCK_ERC20_ABI = json.loads(data['result'])

    def __init__(self):
        """
        Initialize an instance of the ERC721Contract class.
        Sets up the web3 instance and the contract.
        """
        self.contract_address = self.MOCK_ERC20_CONTRACT_ADDRESS
        self.w3 = Web3(Web3.HTTPProvider(self.PROVIDER_URL))
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.MOCK_ERC20_ABI
        )

    def get_contract_instance(self):
        """
        Get the ERC20 contract instance.

        Returns:
            Contract: An instance of the ERC20 smart contract.
        """
        return self.contract

    def mint(self, owner_address, amount):
        """
        Create a minting transaction for the ERC20 contract.

        Args:
            owner_address (str): The address of the owner to receive the minted tokens.
            amount (int): The amount of tokens to mint.

        Returns:
            dict: A dictionary representing the minting transaction.
        """
        txn = self.contract.functions.mint(owner_address, int(amount)).build_transaction({
            'chainId': int(config("CHAIN_ID")),
            'gas': int(config("GAS_LIMIT")),
            'gasPrice': self.w3.to_wei('20', 'gwei'),
            'nonce': self.w3.eth.get_transaction_count(owner_address)
        })

        return txn

    def approve(self, spender_address, amount):
        """
        Create an approval transaction for the ERC20 contract.

        Args:
            spender_address (str): The address of the spender to approve for spending tokens.
            amount (int): The amount of tokens to approve for spending.

        Returns:
            dict: A dictionary representing the approval transaction.
        """
        txn = self.contract.functions.approve(
            spender_address, int(amount)).build_transaction(
            {
                'chainId': int(
                    config("CHAIN_ID")), 'gas': int(
                    config("GAS_LIMIT")), 'gasPrice': self.w3.to_wei(
                        '20', 'gwei'), 'nonce': self.w3.eth.get_transaction_count(
                            config('COLLECTOR_ADDRESS'))})

        return txn


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

    def get_contract_instance(self):
        """
        Get the ERC721 contract instance.

        Returns:
            Contract: An instance of the ERC721 smart contract.
        """
        return self.contract

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

    def mint(self, owner_address):
        """
        Create a minting transaction for the ERC721 contract.

        Args:
            owner_address (str): The address of the owner to receive the minted token.

        Returns:
            dict: A dictionary representing the minting transaction.
        """
        txn = self.contract.functions.mint(owner_address).build_transaction({
            'chainId': int(config("CHAIN_ID")),
            'gas': int(config("GAS_LIMIT")),
            'gasPrice': self.w3.to_wei('20', 'gwei'),
            'nonce': self.w3.eth.get_transaction_count(owner_address)
        })

        return txn

    def set_approval_for_all(self):
        """
        Create an approval transaction to set marketplace approval for all tokens.

        Returns:
            dict: A dictionary representing the approval transaction.
        """
        txn = self.contract.functions.set_approval_for_all(
            config('MARKETPLACE_ADDRESS'), True).build_transaction(
            {
                'chainId': int(
                    config("CHAIN_ID")), 'gas': int(
                    config("GAS_LIMIT")), 'gasPrice': self.w3.to_wei(
                        '20', 'gwei'), 'nonce': self.w3.eth.get_transaction_count(
                            config('ARTIST_ADDRESS'))})

        return txn


class MarketplaceContract:
    """
    A class to interact with the Marketplace smart contract on the Ethereum blockchain.

    Attributes:
        PROVIDER_URL (str): The Ethereum network provider's URL.
        MARKETPLACE_ADDRESS (str): The Ethereum address of the Marketplace contract.
        MARKETPLACE_ABI_PATH (str): Path to the ABI (Application Binary Interface) of
            the Marketplace contract.
        MARKETPLACE_ABI (list): Loaded ABI content from the JSON file.
    """
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
        """
        Send a transaction to the Marketplace contract to finish an auction.

        Args:
            nft_collection_address (str): The address of the NFT collection.
            token_id (int): The ID of the NFT token.
            erc20_address (str): The address of the ERC20 token.
            erc20_amount (int): The amount of ERC20 tokens.
            bidder_sig (str): The signature of the bidder.
            owner_approval_sig (str): The signature of the owner's approval.
            owner_address (str): The address of the owner.

        Returns:
            dict: The transaction object.
        """

        # Decompose the auction_data dictionary into a tuple
        auction_tuple = (
            nft_collection_address,
            erc20_address,
            int(token_id),  # ensure it's an integer (uint256)
            int(erc20_amount)  # ensure it's an integer (uint256)
        )

        # Send the transaction
        txn = self.contract.functions.finishAuction(
            auction_tuple,
            bidder_sig,
            owner_approval_sig
        ).build_transaction({
            'chainId': int(config("CHAIN_ID")),
            'gas': int(config("GAS_LIMIT")),
            'gasPrice': self.w3.to_wei('20', 'gwei'),
            'nonce': self.w3.eth.get_transaction_count(owner_address)
        })

        return txn
