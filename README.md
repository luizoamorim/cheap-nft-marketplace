Cheap NFT Marketplace
A decentralized NFT marketplace built on the Sepolia network, enabling NFT holders to securely list and trade their tokens.

🛠 Technologies Used
Python: A powerful, dynamic language we're using for backend logic.

Django: A high-level Python web framework that encourages rapid design and a clean, pragmatic design. We're using Django to design our REST API and manage our backend logic.

Solidity: A statically-typed programming language for writing smart contracts on the Ethereum blockchain. We're deploying our smart contracts on the Sepolia testnet.

Sepolia Network: A testnet where our smart contracts are deployed and tested.

📝 Smart Contracts
Settler Contract: Enables two users to securely settle their trades in a decentralized way using a single transaction.

MockERC20: A mock contract for testing purposes that simulates an ERC20 token. Users can mint any amount for testing.

MockERC721: A mock contract for testing purposes that simulates an ERC721 token (NFT). Users can mint any token for testing.

🔗 Endpoints
List NFT
URL: /list/
Method: POST
Data Params:
collectionAddress: Address of the NFT contract
tokenId: ID of the specific NFT token
price: Listing price or initial auction price
isAuction: A boolean indicating if it's an auction (optional, default is false)
Success Response:
Code: 201
Content: { message: "Listing added successfully" }
Use a GET request on this endpoint to retrieve a JSON response containing all the current NFT listings.

🚀 Installation and Setup
Clone the Repository:
bash
Copy code
git clone https://github.com/luizoamorim/cheap-nft-marketplace.git
Install Dependencies:
Ensure you're in the project directory, then:
bash
Copy code
pip install -r requirements.txt
Run Migrations:
bash
Copy code
python manage.py migrate
Run the Development Server:
bash
Copy code
python manage.py runserver
Navigate to http://127.0.0.1:8000/ in your browser.

🧪 Testing
Ensure you have all dependencies installed, then run:

bash
Copy code
python manage.py test marketplace
🤝 Contribute
Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.
