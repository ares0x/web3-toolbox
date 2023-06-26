from web3 import Web3
from eth_account import Account

# 生成 ETH 地址
def createAccount():
    w3 = Web3(); 
    # create 中的参数extra_entropy 也可以删除 
    acc = w3.eth.account.create(extra_entropy='ares0xff')
    # 将生成的 eth 地址导入 metamask 等软件即可
    print(f'privateKey:{w3.to_hex(acc.key)}, account:{acc.address}')

# 批量生成地址
def createAccounts(quantity):
    Account.enable_unaudited_hdwallet_features()
    result = Account.create_with_mnemonic(passphrase = 'fucksec')
    mnemonic = result[1]
    wallets = []
    print(mnemonic)
    for index in range(quantity):
        localAccount = Account.from_mnemonic(mnemonic=mnemonic,
                                             account_path="m/44'/60'/0'/0/"+ str(index))
        privateKey = str.lower(bytes_to_hex(localAccount.key))
        address = localAccount.address
        wallet = {
            "id": index,
            "address": address,
            "privateKey": privateKey,
            "mnemonic": mnemonic
        }
        wallets.append(wallet.values())

    print(wallets)
    # return wallets
    
def bytes_to_hex(bs):
    return ''.join(['%02X' % b for b in bs])


def main():
    # createAccount()
    createAccounts(5)

if __name__ == "__main__":
    main()
