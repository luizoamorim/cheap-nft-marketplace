#!/bin/bash

# Echo script commands for better visibility
set -x

# Mint ERC20 tokens
echo "Minting ERC20 tokens..."
python3 ./marketplace/test/e2e/mintERC20.py 
sleep 30  # wait for 30 seconds

# Approve ERC20 tokens for spending
echo "Approving ERC20 tokens..."
python3 ./marketplace/test/e2e/erc20Approve.py
sleep 30  # wait for 30 seconds

# Set approval for all
echo "Setting approval for all..."
python3 ./marketplace/test/e2e/setApprovalForAll.py 
sleep 30  # wait for 30 seconds

# Purchase operation
echo "Initiating purchase..."
python3 ./marketplace/test/e2e/purchase.py 

echo "E2E test sequence completed!"