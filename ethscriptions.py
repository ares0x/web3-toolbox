import os
import csv
from web3 import Web3
from dotenv import load_dotenv
_ = load_dotenv()

INFURA_SECRET_KEY = os.environ['INFURA_SECRET_KEY']
PRIVATE_KEY = os.environ['ETH_MAINNET_PRIVATE_KEY']
ADDRESS = os.environ['ETH_MAINNET_ADDRESS']
CSV_PATH = 'eths.csv'

base_content = 'data:,{"p":"erc-20","op":"mint","tick":"eths","id":"0","amt":"1000"}'
contents = ['','']
def get_w3_by_network(network='mainnet'):
    infura_url = f'https://{network}.infura.io/v3/{INFURA_SECRET_KEY}' 
    w3 = Web3(Web3.HTTPProvider(infura_url))
    return w3

# 思路：文本内容是固定的，即 id 最大21000，所以可以预先生成所有文本的哈希
# 去重的思路是获取区块详情 -》 获取交易详情 -》 判断交易的 input 时候有相同的数据
# 完整的步骤：
# 1. 预生成所有的16进制
# 2. 从产生类似交易的第一个区块高度开始轮训所有的区块，获取区块中的所有交易
# 3. 分别解析区块中的交易中的 input 是否包含之前生成的内容，如果包含了，啧将其标记为已存在，然后继续轮训交易。当该块中的所有交易已经轮训完时，解析下一个块
# 4. 最后我们可以得到一份已经去重的16进制内容，此时我们只需要将其放在构造的交易结构中的 data 部分，并发送 amount 为 0 到自己的地址，即可在很大程度上减少重复的概率

# generateAndSave 用于生成所有的 16 进制，并保存在 csv 中
def generateAndSave():
    inputs = []
    for id_num in range(1, 21001):
        id_str = str(id_num)
        replaced_string = base_content.replace('"id":"0"', f'"id":"{id_str}"')
        content = replaced_string.encode('utf-8').hex()
        full_content = '0x'+ content
        wallet = {
            "id": id_num,
            "content": replaced_string,
            "byte": full_content,
            "state":0 # 0表示初始状态或者未打状态，已经存在的会被更新为1
        }
        inputs.append(wallet.values())
    saveContentToCsv(inputs)

# saveContentToCsv 保存到 csv 中
def saveContentToCsv(jsonData):
    with open(CSV_PATH, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["ID","内容", "16进制","状态"])
        csv_writer.writerows(jsonData)

# 解析交易 判断 input 中是否包含该数据
# def parseTx():
#     w3 = get_w3_by_network('mainnet')
#     transaction = w3.eth.get_transaction(txHash)
#     input_data = transaction.input
#     compare_content = 'data:,{"p":"erc-20","op":"mint","tick":"eths","id":"20999","amt":"1000"}'
#     content = compare_content.encode('utf-8').hex()
#     full_content = '0x'+ content
#     print(f'交易中的input:',{input_data},'生成的content:',{full_content})
#     if input_data == input_data:
#         print('该交易包含特定数据。')
#     else:
#         print('该交易不包含特定数据。')

    
def estimated_price(w3):
    gas_price = w3.eth.gas_price
    gas_price_gwei = w3.from_wei(gas_price, 'gwei')
    print("Current gas price (Gwei):", gas_price_gwei)
    return gas_price_gwei

# def rollUpBlock(baseBlockNum=10000):
    
# baseBlockNum 默认设置为该项目产生交易的第一个区块
def getBlockDetail(w3):
    baseBlockNum=17488109
    latest_block = w3.eth.get_block(baseBlockNum)
    while True:
        for tx_hash in latest_block.transactions:
            transaction = w3.eth.get_transaction(tx_hash)
            input_data = transaction.input
            amount = w3.from_wei(transaction['value'], 'ether')
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
            if input_data == '':
                continue
            if readAccountFromCsv(input_data) == False:
                continue
            print(f'Transaction Hash:', {tx_hash.hex()})
        baseBlockNum = baseBlockNum + 1


def readAccountFromCsv(target_data):
    with open(CSV_PATH, 'r') as file:
        reader = csv.DictReader(file)
        # 遍历每一行数据
        for row in reader:
            # 对比目标数据与目标列的值
            if target_data == row["16进制"]:
                print('已经存在了该内容,16 进制:',{target_data})
                return True 
        return False

# batchTransfer 批量发送交易
def batchTransfer(w3,from_address,private_key,target_address, chainId, data,amount = 0,gas_limit=35000):
    gasPrice = estimated_price(w3) * 1.3
    transactions = []
    nonce = w3.eth.get_transaction_count(from_address)
    for c in contents:
        tx = {
            'from': from_address,
            'nonce': nonce,
            'to': target_address,
            'value': w3.to_wei(amount, 'ether'),
            'gas': gas_limit,
            'maxFeePerGas': w3.to_wei(gasPrice, 'gwei'),
            'maxPriorityFeePerGas': w3.to_wei(gasPrice, 'gwei'),
            'chainId': chainId,
        }
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
        transactions.append(signed_tx)
        nonce = nonce + 1

    for raw_tx in transactions:
        try:
            taHash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            return {'status': 'succeed', 'txn_hash': w3.to_hex(taHash), 'task': 'Transfer ETH'}
        except Exception as e:
            return {'status': 'failed', 'error': e, 'task': 'Transfer ETH'}

def main():
    w3 = get_w3_by_network('mainnet')
    # 生成哈希并保存到 csv 中
    generateAndSave()

    # 读取区块
    getBlockDetail(w3)
    # parseTx()
    # 判断时候存在如果没有，则将其放在另外一个csv文件中
    
    # 便利新生成的csv，分别发送交易
    
    # content = ''
    # result = batchTransfer(w3, ADDRESS, PRIVATE_KEY, ADDRESS,chainId=1,data=content)
    # print(result)
    


if __name__ == "__main__":
    main()