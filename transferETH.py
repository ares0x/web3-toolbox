import os
from web3 import Web3, middleware
from dotenv import load_dotenv
_ = load_dotenv()

INFURA_SECRET_KEY = os.environ['INFURA_SECRET_KEY']
PRIVATE_KEY = os.environ['ETH_MAINNET_PRIVATE_KEY']
ADDRESS = os.environ['ETH_MAINNET_ADDRESS']
TARGET_ADDRESS = '0xb28B1f403284de535F5959bd590bBF344d0B0948'

def get_w3_by_network(network='mainnet'):
    infura_url = f'https://{network}.infura.io/v3/{INFURA_SECRET_KEY}' 
    w3 = Web3(Web3.HTTPProvider(infura_url))
    return w3


def transfer_eth(w3,from_address,private_key,target_address,amount,gas_price=5,gas_limit=21000,chainId=4):
    from_address = Web3.to_checksum_address(from_address)
    target_address = Web3.to_checksum_address(target_address)
    nonce = w3.eth.get_transaction_count(from_address) # 获取 nonce 值
    params = {
        'from': from_address,
        'nonce': nonce,
        'to': target_address,
        'value': w3.to_wei(amount, 'ether'),
        'gas': gas_limit,
        'maxFeePerGas': w3.to_wei(gas_price, 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei(gas_price, 'gwei'),
        'chainId': chainId,
        
    }
    try:
        signed_tx = w3.eth.account.sign_transaction(params, private_key=private_key)
        taHash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return {'status': 'succeed', 'txn_hash': w3.to_hex(taHash), 'task': 'Transfer ETH'}
    except Exception as e:
        return {'status': 'failed', 'error': e, 'task': 'Transfer ETH'}
    
# 注意，可能使用此方法获取到的 gasPrice 会偏低，导致交易不容易被打包
def estimated_price(w3):
    gas_price = w3.eth.gas_price
    gas_price_gwei = w3.from_wei(gas_price, 'gwei')
    print("Current gas price (Gwei):", gas_price_gwei)
    return gas_price_gwei

def main():
    w3 = get_w3_by_network('mainnet')
    amount = 0.005
    balance = w3.eth.get_balance(ADDRESS) / 1e18
    print(f'当前地址余额: {balance = } ETH')
    gasPrice = estimated_price(w3)
    
    result = transfer_eth(w3, ADDRESS, PRIVATE_KEY, TARGET_ADDRESS, amount,gas_price=gasPrice,chainId=1)
    print(result)
    

if __name__ == "__main__":
    main()
