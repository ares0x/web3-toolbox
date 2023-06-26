import os
from web3 import Web3
from dotenv import load_dotenv
_ = load_dotenv()

INFURA_SECRET_KEY = os.environ['INFURA_SECRET_KEY']
PRIVATE_KEY = os.environ['ETH_MAINNET_PRIVATE_KEY']
ADDRESS = os.environ['ETH_MAINNET_ADDRESS']



def get_w3_by_network(network='mainnet'):
    infura_url = f'https://{network}.infura.io/v3/{INFURA_SECRET_KEY}' 
    w3 = Web3(Web3.HTTPProvider(infura_url))
    return w3

def monitorBlock(w3):
    latest_block_number = w3.eth.block_number
    print(f'current block:',latest_block_number)
    while True:
        block = w3.eth.get_block(latest_block_number)
        for tx_hash in block.transactions:
            transaction = w3.eth.get_transaction(tx_hash)
            amount = w3.from_wei(transaction['value'], 'ether')
            input_data = transaction.input
            if amount > 0 or input_data == '' or input_data == '0x':
                continue
            is_contract_call = len(input_data) >= 10 and input_data[:2] != '0x'
            if is_contract_call:
                continue
            hex_string = input_data[2:]
            # 判断长度是否为偶数
            if len(hex_string) % 2 != 0:
                print('Invalid hex string length')
                continue
            # print(input_data)
            try:
                input = bytes.fromhex(hex_string).decode('utf-8')
                # 这里可以对转换成功的字符串进行处理
                # print("有效的 UTF-8 字符串:", input)
                print(f"Transaction Hash:", {tx_hash.hex()}, "input:",input)
            except UnicodeDecodeError:
                continue
                # print("乱码数据:", hex_string)
                # print(f"Transaction Hash:", {tx_hash.hex()}, "input:",input)
            
        latest_block_number = latest_block_number + 1


def main():
    w3 = get_w3_by_network('mainnet')
    monitorBlock(w3)
    # # 生成哈希并保存到 csv 中
    # generate() 
    # # 读取区块
    # # parseTx()
    # # 判断时候存在如果没有，则将其放在另外一个csv文件中
    
    # # 便利新生成的csv，分别发送交易
    
    # content = ''
   
    # amount = 0
    # gasPrice = estimated_price(w3) * 1.3
    # result = transfer_eth(w3, ADDRESS, PRIVATE_KEY, ADDRESS, amount,gas_price=gasPrice,chainId=1,data=content)
    # print(result)
    


if __name__ == "__main__":
    main()