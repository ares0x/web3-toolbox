# web3-toolbox
该项目灵感来源于 [Web3_Tutoria](https://github.com/gm365/Web3_Tutorial)。在该项目下有一些常用的代码片段，这些代码片段涵盖了日常交易过程中的常用操作：

* [生成eth地址](./account.py)
* [eth转账-转eth到账户](./transferETH.py)
* [eths铭文](./ethscriptions.py)
* [监控交易中的input数据](./monitor_input.py)
* [vmpx mint](./vmpx.py)

## 注意
1. 使用该项目下的代码，首先需要创建一个名为 .env 的文件，在该文件中写入
```env
INFURA_SECRET_KEY = [YOUR_INFURA_KEY]
```
INFURA_KEY 需要自己去 [infura](https://www.infura.io/zh) 申请

2. 对于该项目中的 .env 文件我在 .gitignore 做了忽略，即它不会被提交到 github 当中。对于一些私钥类的常量，建议采用相同的方式提取到 .env 中，以防私钥泄露

## 参考资料
[web3.py](https://web3py.readthedocs.io/en/stable/index.html)