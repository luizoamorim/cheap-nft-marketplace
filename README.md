# Cheap NFT Marketplace

A decentralized NFT marketplace built on the Sepolia network, enabling NFT holders to securely list and trade their tokens.

## 🛠 Technologies Used

**Python**: A powerful, dynamic language we're using for backend logic.

**Django**: A high-level Python web framework that encourages rapid design and a clean, pragmatic design. We're using Django to design our REST API and manage our backend logic.

**Solidity**: A statically-typed programming language for writing smart contracts on the Ethereum blockchain. We're deploying our smart contracts on the Sepolia testnet.

**Sepolia Network**: A testnet where our smart contracts are deployed and tested.

## 📝 Smart Contracts

1. **Settler Contract**: Enables two users to securely settle their trades in a decentralized way using a single transaction.

2. **MockERC20**: A mock contract for testing purposes that simulates an ERC20 token. Users can mint any amount for testing.

3. **MockERC721**: A mock contract for testing purposes that simulates an ERC721 token (NFT). Users can mint any token for testing.

## 🔗 Endpoints

### List NFT

#### - URL: /list/

#### - Method: POST

#### - Data Params:

- **collectionAddress**: Address of the NFT contract
- **tokenId**: ID of the specific NFT token
- **price**: Listing price or initial auction price
- **isAuction**: A boolean indicating if it's an auction (optional, default is false)

#### - \*\*Success Response:

- **Code**: 201
- **Content**: { message: "Listing added successfully" }

Use a **GET** request on this endpoint to retrieve a JSON response containing all the current NFT listings.

### Purchase Order

#### - URL: /purchase_order/

#### - Method: POST

#### - Data Params:

**nft_collection_address:** Address of the NFT contract
**tokenId:** ID of the specific NFT token
**erc20Address:** Address of the ERC20 token used for payment
**erc20_amount:** The amount of ERC20 tokens for the purchase
**bidderSig:** Signature of the buyer for the purchase
**buyerAddress:** Address of the buyer
**sale_id:** Sale ID of the NFT listing

#### - Success Response:

**Code:** 200
**Content:** { "message": "Purchase initiated" }

### Bid Order

#### - URL: /bid_order/

#### - Method: POST

#### - Data Params:

**nft_collection_address:** Address of the NFT contract
**tokenId:** ID of the specific NFT token
**erc20Address:** Address of the ERC20 token used for bidding
**erc20_amount:** The amount of ERC20 tokens for the bid
**bidderSig:** Signature of the bidder
**buyerAddress:** Address of the bidder
**sale_id:** Sale ID of the NFT auction listing

#### - Success Response:

**Code:** 200
**Content:** { "message": "Bid placed" }

### Settle Purchase Order

#### - URL: /settle_purchase_order/

#### - Method: POST

#### - Data Params:

**sale_id:** Sale ID of the NFT listing
**owner_approval_sig:** Signature of the owner for the purchase approval
**owner_address:** Address of the owner

#### - Success Response:

**Code:** 200
**Content:** { "message": "Transaction successful created.", "txHash": tx_hash }

### Settle Auction Order

#### - URL: /settle_auction_order/

#### - Method: POST

#### - Data Params:

**sale_id:** Sale ID of the NFT auction listing
**owner_approval_sig:** Signature of the owner for the auction settlement
**owner_address:** Address of the owner

### - Success Response:

**Code:** 200
**Content:** { "message": "Transaction successfully created.", "txHash": tx_hash }

These endpoints allow you to list NFTs, initiate purchases, place bids, and settle both purchase and auction orders in your NFT marketplace.

## 🚀 Installation and Setup

#### 1. Clone the Repository:

```
git clone https://github.com/luizoamorim/cheap-nft-marketplace.git
```

#### 2. Setting up .env using MetaMask and Infura:

Create a .env file based on the .env_sample file.

##### Contract Addresses (No change here):

**MOCK_ERC721_CONTRACT_ADDRESS:** Address of the deployed mock ERC721 token contract.
**MOCK_ERC20_CONTRACT_ADDRESS:** Address of the deployed mock ERC20 token contract.
**MARKETPLACE_ADDRESS:** Address of the deployed marketplace contract.

##### Ethereum Node / Network Details:

**PROVIDER_URL:** For using Infura, you need to sign up for a free account on Infura. After creating your project, you'll be provided with an endpoint URL for the Sepolia network. It will look something like: https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID.

**CHAIN_ID:** For Sepolia testnet the chain ID is 11155111.

**GAS_LIMIT:** You can leave this as 8000000 or adjust based on your needs.

##### User (Artist/Collector) Specifics using MetaMask:

**Artist:**
Open MetaMask and select your desired address for the artist.
Click on the account details (icon with three dots) and select "Account details".
Here you can see and copy the Ethereum address (**ARTIST_ADDRESS**).

**Private Key (Use with caution):**
In the same account detail view, there is an option to "Export Private Key". Click on it, provide your MetaMask password and you'll see your private key (**ARTIST_PRIVATE_KEY**). Never share this key and use it carefully.
Collector:

##### Follow the same steps as the artist but choose/select a different MetaMask address.

This will give you the **COLLECTOR_ADDRESS** and **COLLECTOR_PRIVATE_KEY**.

##### Other (No change here):

TOKEN_ID: Below we'll show hot to get the correct one.
BASE_URL: The base URL of your application. If you're running locally, this will be http://127.0.0.1:8080.

#### Important Notes:

**Security:** Be extremely cautious when dealing with private keys. Never share them, and always make sure you are exporting or inputting them in secure environments.
**MetaMask:** It's good practice to frequently back up your MetaMask seed phrase in a secure location. Also, when exporting private keys from MetaMask, make sure you're not in a compromised environment or have any malicious browser extensions that might capture your activities.
**Infura:** The provided URL should be kept secure. Avoid sharing your Infura Project ID publicly.
**Environment File:** Never commit or push the .env file with real private keys or sensitive information to public repositories.

#### 3. Install Dependencies:

Ensure you're in the project directory, then:

```
pip install -r requirements.txt
```

#### 4. 🧪 Testing

```
run_tests.sh
```

#### 5. Run the ERC721 listner to see the TokenID minted:

```
./run_erc721_listners.sh
```

#### 6. Mint the ERC721 for the Artist added to the .env:

Run this on a separated terminal:

```
./run_mint_nft.sh
```

You should see something like this:

```
Signed txn:  SignedTransaction(rawTransaction=HexBytes('0xf88f8201838504a817c800837a120094fce9b92ec11680898c7fe57c4ddcea83aeaba3ff80a46a627842000000000000000000000000929a4dfc610963246644b1a7f6d1aed40a27dd2f8401546d71a066fe40559cbc28b04ebf41bd0ef2600d625532829e52145a1c08d4f6db92c9fca05d247f464fa51ebcc28a6f37510447652aa5893f8587e99c786d1f7d2bb09cd8'), hash=HexBytes('0x708f60b4258116bc5254f96ea9aa2453e3e73a4cd55b50f3b992913116fb1517'), r=46585133729814664136391567068398691202126905005405950464128578140273118464508, s=42129579829945702554542032512941708321478437660954237310232932972708685192408, v=22310257)
Transaction hash: 0x708f60b4258116bc5254f96ea9aa2453e3e73a4cd55b50f3b992913116fb1517
```

On the terminal running the listner, you should see something like that:

```
ERC721 listening...
AttributeDict({'args': AttributeDict({'from': '0x0000000000000000000000000000000000000000', 'to': '0x929A4DfC610963246644b1A7f6D1aed40a27dD2f', 'tokenId': 230}), 'event': 'Transfer', 'logIndex': 0, 'transactionIndex': 0, 'transactionHash': HexBytes('0x2fa1bcc7195597ab9b9e4c4bb05afad929e647d8df6b1095f04c81604cc11777'), 'address': '0xFCE9b92eC11680898c7FE57C4dDCea83AeabA3ff', 'blockHash': HexBytes('0x23a852eb59006ebec97eae63fedc5bdfadbb2e5f110cb970c1a891c260e321ea'), 'blockNumber': 4498104})
```

See that it shows the tokenId: 230

#### 7. Add the token id number (230) that you see on the listner terminal to the .env:

TOKEN_ID=230

#### 8. Run the Development Server:

```
python manage.py runserver
```

You should see something like that:

```
Starting development server at http://127.0.0.1:8080/
Quit the server with CONTROL-C.
```

Navigate to http://127.0.0.1:8000/ in your browser.

#### 8. Run the e2e script:

- It will mint the quantity necessary of ERC20 for the Collector.
- Will allow the marketplace exchange these tokens on collector's behalf.
- Will call the ERC721 setApprovalForAll on artist's name for the marketplace.
- Will call the purchase end to end script.

#### 9. Purchase

- Sends a POST request to the /list/ endpoint of your NFT marketplace to list an NFT. It takes the NFT data as input, sends the request, and returns the JSON response.
- Initiate the purchase of an NFT. It creates a message to be signed, signs the message with the collector's private key, updates the data with the signature and buyer address, and sends a POST request to the /purchaseOrder/ endpoint. It then prints the response and returns the data.
- Settle the purchase order. It takes the sale ID and the collector's signature as input, signs the settlement request with the artist's private key, sends a POST request to the /settle_purchase_order/ endpoint, and returns the JSON response.

In the main part of the script, you first list an NFT, then purchase it, and finally settle the purchase order. It includes steps such as sending the signed transaction to the Ethereum blockchain.

Please note that this script assumes that the listed NFT is being purchased by a collector and settled by an artist, and it uses their respective private keys and addresses for signing and verification. The script also relies on your NFT marketplace's API endpoints for listing, purchasing, and settling NFTs.

## Results

On the final you should see something like that:

### Server running terminal

```
Starting development server at http://127.0.0.1:8080/
Quit the server with CONTROL-C.

[15/Oct/2023 05:38:08] "POST /list/ HTTP/1.1" 201 54
[15/Oct/2023 05:38:08] "POST /purchaseOrder/ HTTP/1.1" 200 33
[15/Oct/2023 05:38:09] "POST /settle_purchase_order/ HTTP/1.1" 200 1116
```

### e2e purchase terminal

```
python3 ./marketplace/test/e2e/purchase.py
Listing Response: {'message': 'Listing added successfully', 'sale_id': 1}
Data to be sent for purchase: {'nft_collection_address': '0xFCE9b92eC11680898c7FE57C4dDCea83AeabA3ff', 'tokenId': '227', 'erc20Address': '0xbd65c58D6F46d5c682Bf2f36306D461e3561C747', 'erc20_amount': 10500000000000000, 'bidderSig': '0x401e4685a98dd9910ac029a352621572f57a41fc49c4ed074f3e7d43e85ca3c5491a0668cfea8fafc210d1cf83f453d8f9b57d78faddc9556e9e768b04c4f28a1b', 'buyerAddress': '0xa1fC57f2Ba9f466b2BB2906dB3a5ea3000bA50C3', 'sale_id': 1}
Purchase Response: {'message': 'Purchase initiated'}
Settle Response: {'message': 'Transaction successful created.', 'txHash': {'value': 0, 'chainId': 11155111, 'gas': 8000000, 'gasPrice': 20000000000, 'nonce': 385, 'to': '0x597C9bC3F00a4Df00F85E9334628f6cDf03A1184', 'data': '0x0f96837b000000000000000000000000fce9b92ec11680898c7fe57c4ddcea83aeaba3ff000000000000000000000000bd65c58d6f46d5c682bf2f36306d461e3561c74700000000000000000000000000000000000000000000000000000000000000e300000000000000000000000000000000000000000000000000254db1c224400000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000000000000000000000000000000041401e4685a98dd9910ac029a352621572f57a41fc49c4ed074f3e7d43e85ca3c5491a0668cfea8fafc210d1cf83f453d8f9b57d78faddc9556e9e768b04c4f28a1b000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000041f116dcf6d661a163e5a9fb54ab1e6f5898dfe974504d752f4278a4190c1683567159f064a44f73d10f706f5154ca8ff5a4d047b039b044f86458d9d202ebc6181c00000000000000000000000000000000000000000000000000000000000000'}}
Signed txn:  SignedTransaction(rawTransaction=HexBytes('0xf902318201818504a817c800837a120094597c9bc3f00a4df00f85e9334628f6cdf03a118480b901c40f96837b000000000000000000000000fce9b92ec11680898c7fe57c4ddcea83aeaba3ff000000000000000000000000bd65c58d6f46d5c682bf2f36306d461e3561c74700000000000000000000000000000000000000000000000000000000000000e300000000000000000000000000000000000000000000000000254db1c224400000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000000000000000000000000000000041401e4685a98dd9910ac029a352621572f57a41fc49c4ed074f3e7d43e85ca3c5491a0668cfea8fafc210d1cf83f453d8f9b57d78faddc9556e9e768b04c4f28a1b000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000041f116dcf6d661a163e5a9fb54ab1e6f5898dfe974504d752f4278a4190c1683567159f064a44f73d10f706f5154ca8ff5a4d047b039b044f86458d9d202ebc6181c000000000000000000000000000000000000000000000000000000000000008401546d72a036321b35e0a991a0d772540d545afe51090d6b29aeb33be6b98b6d4c282e6ff8a06c44eee79d4416742f4e9bf122ad0823dc5d01f2533db8ade689a627ffa832e9'), hash=HexBytes('0x05347e75ec05e84b9bd1717aba6df3b6eaf9be60926632dfa1a29f9e1f01872b'), r=24513423976423550809783900511060536053472284921845770381885597160286475677688, s=48971582107337955796088555294794929909698061325818930577038783745893868253929, v=22310258)
Transaction hash: 0x05347e75ec05e84b9bd1717aba6df3b6eaf9be60926632dfa1a29f9e1f01872b
```

### Running listner terminal

```
python3 ./marketplace/events/ERC721listeners.py
ERC721 listening...
AttributeDict({'args': AttributeDict({'from': '0x929A4DfC610963246644b1A7f6D1aed40a27dD2f', 'to': '0xa1fC57f2Ba9f466b2BB2906dB3a5ea3000bA50C3', 'tokenId': 227}), 'event': 'Transfer', 'logIndex': 2, 'transactionIndex': 0, 'transactionHash': HexBytes('0x05347e75ec05e84b9bd1717aba6df3b6eaf9be60926632dfa1a29f9e1f01872b'), 'address': '0xFCE9b92eC11680898c7FE57C4dDCea83AeabA3ff', 'blockHash': HexBytes('0x0edf3e336b2a57c8ed3fa2689b92c5715fc6b9b401b434ee2e52be34d010128d'), 'blockNumber': 4493097})
```

### Tenderly

You can also use a service like Tenderly. You can add the contract for the Sepolia Network and check the transactions:

![image](https://github.com/luizoamorim/cheap-nft-marketplace/assets/73957838/2604e740-2a2b-4ec6-949c-b620c5a97f5e)

## 🤝 Contribute

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.
