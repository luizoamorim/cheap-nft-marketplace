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

#### 3. Run Migrations:

```
python manage.py migrate
```

#### 4. Run the Development Server:

```
python manage.py runserver
```

#### 4. Run the Development Server:

```
python manage.py runserver
```

Navigate to http://127.0.0.1:8000/ in your browser.

## 🧪 Testing

Ensure you have all dependencies installed, then run:

```
python manage.py test marketplace
```

## Results

On the final you should see something like that:

```
Starting development server at http://127.0.0.1:8080/
Quit the server with CONTROL-C.

[15/Oct/2023 05:38:08] "POST /list/ HTTP/1.1" 201 54
[15/Oct/2023 05:38:08] "POST /purchaseOrder/ HTTP/1.1" 200 33
[15/Oct/2023 05:38:09] "POST /settlePurchaseOrder/ HTTP/1.1" 200 1116
```

```
python3 ./marketplace/test/e2e/purchase.py
Listing Response: {'message': 'Listing added successfully', 'saleId': 1}
Data to be sent for purchase: {'nftCollectionAddress': '0xFCE9b92eC11680898c7FE57C4dDCea83AeabA3ff', 'tokenId': '227', 'erc20Address': '0xbd65c58D6F46d5c682Bf2f36306D461e3561C747', 'erc20Amount': 10500000000000000, 'bidderSig': '0x401e4685a98dd9910ac029a352621572f57a41fc49c4ed074f3e7d43e85ca3c5491a0668cfea8fafc210d1cf83f453d8f9b57d78faddc9556e9e768b04c4f28a1b', 'buyerAddress': '0xa1fC57f2Ba9f466b2BB2906dB3a5ea3000bA50C3', 'saleId': 1}
Purchase Response: {'message': 'Purchase initiated'}
Settle Response: {'message': 'Transaction successful created.', 'txHash': {'value': 0, 'chainId': 11155111, 'gas': 8000000, 'gasPrice': 20000000000, 'nonce': 385, 'to': '0x597C9bC3F00a4Df00F85E9334628f6cDf03A1184', 'data': '0x0f96837b000000000000000000000000fce9b92ec11680898c7fe57c4ddcea83aeaba3ff000000000000000000000000bd65c58d6f46d5c682bf2f36306d461e3561c74700000000000000000000000000000000000000000000000000000000000000e300000000000000000000000000000000000000000000000000254db1c224400000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000000000000000000000000000000041401e4685a98dd9910ac029a352621572f57a41fc49c4ed074f3e7d43e85ca3c5491a0668cfea8fafc210d1cf83f453d8f9b57d78faddc9556e9e768b04c4f28a1b000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000041f116dcf6d661a163e5a9fb54ab1e6f5898dfe974504d752f4278a4190c1683567159f064a44f73d10f706f5154ca8ff5a4d047b039b044f86458d9d202ebc6181c00000000000000000000000000000000000000000000000000000000000000'}}
Signed txn:  SignedTransaction(rawTransaction=HexBytes('0xf902318201818504a817c800837a120094597c9bc3f00a4df00f85e9334628f6cdf03a118480b901c40f96837b000000000000000000000000fce9b92ec11680898c7fe57c4ddcea83aeaba3ff000000000000000000000000bd65c58d6f46d5c682bf2f36306d461e3561c74700000000000000000000000000000000000000000000000000000000000000e300000000000000000000000000000000000000000000000000254db1c224400000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000000000000000000000000000000041401e4685a98dd9910ac029a352621572f57a41fc49c4ed074f3e7d43e85ca3c5491a0668cfea8fafc210d1cf83f453d8f9b57d78faddc9556e9e768b04c4f28a1b000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000041f116dcf6d661a163e5a9fb54ab1e6f5898dfe974504d752f4278a4190c1683567159f064a44f73d10f706f5154ca8ff5a4d047b039b044f86458d9d202ebc6181c000000000000000000000000000000000000000000000000000000000000008401546d72a036321b35e0a991a0d772540d545afe51090d6b29aeb33be6b98b6d4c282e6ff8a06c44eee79d4416742f4e9bf122ad0823dc5d01f2533db8ade689a627ffa832e9'), hash=HexBytes('0x05347e75ec05e84b9bd1717aba6df3b6eaf9be60926632dfa1a29f9e1f01872b'), r=24513423976423550809783900511060536053472284921845770381885597160286475677688, s=48971582107337955796088555294794929909698061325818930577038783745893868253929, v=22310258)
Transaction hash: 0x05347e75ec05e84b9bd1717aba6df3b6eaf9be60926632dfa1a29f9e1f01872b
```

```
python3 ./marketplace/events/ERC721listeners.py
ERC721 listening...
AttributeDict({'args': AttributeDict({'from': '0x929A4DfC610963246644b1A7f6D1aed40a27dD2f', 'to': '0xa1fC57f2Ba9f466b2BB2906dB3a5ea3000bA50C3', 'tokenId': 227}), 'event': 'Transfer', 'logIndex': 2, 'transactionIndex': 0, 'transactionHash': HexBytes('0x05347e75ec05e84b9bd1717aba6df3b6eaf9be60926632dfa1a29f9e1f01872b'), 'address': '0xFCE9b92eC11680898c7FE57C4dDCea83AeabA3ff', 'blockHash': HexBytes('0x0edf3e336b2a57c8ed3fa2689b92c5715fc6b9b401b434ee2e52be34d010128d'), 'blockNumber': 4493097})
```

![image](https://github.com/luizoamorim/cheap-nft-marketplace/assets/73957838/2604e740-2a2b-4ec6-949c-b620c5a97f5e)

## 🤝 Contribute

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.
