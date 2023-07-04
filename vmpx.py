# vmpx https://etherscan.io/address/0xb48Eb8368c9C6e9b0734de1Ef4ceB9f484B80b9C#code

import os
import json
from web3 import Web3
from dotenv import load_dotenv
_ = load_dotenv()


INFURA_SECRET_KEY = os.environ['INFURA_SECRET_KEY']
PRIVATE_KEY = os.environ['ETH_MAINNET_PRIVATE_KEY']
ADDRESS = os.environ['ETH_MAINNET_ADDRESS']

# 配置合约地址和私钥
contract_address = '0xb48Eb8368c9C6e9b0734de1Ef4ceB9f484B80b9C'


def get_w3_by_network(network='mainnet'):
    infura_url = f'https://{network}.infura.io/v3/{INFURA_SECRET_KEY}' 
    w3 = Web3(Web3.HTTPProvider(infura_url))
    return w3

with open('./vmpx.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)

def mint(power,w3):
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    account = w3.eth.account.from_key(PRIVATE_KEY)
    w3.eth.default_account = account.address
    print(contract.aa,account.address)

    try:
        # 调用合约的 mint 函数
        tx_hash = contract.functions.mint(power).transact()

        # 等待交易被确认
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        print('Transaction hash:', tx_receipt.transactionHash.hex())
    except Exception as e:
        print('Minting failed:', str(e))

def main():
    w3 = get_w3_by_network('mainnet')
    mint(1,w3)

if __name__ == "__main__":
    main()