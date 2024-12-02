import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from binance.client import Client
from datetime import datetime, timedelta

class BinanceCryptoEcosystemAnalyzer:
    def __init__(self, api_key=None, api_secret=None, cryptos=None):
        """
        初始化Binance加密货币生态系统分析器
        
        :param api_key: Binance API密钥
        :param api_secret: Binance API秘钥
        :param cryptos: 待分析的加密货币列表
        """
        # 初始化Binance客户端
        self.client = Client(api_key, api_secret)
        
        # 如果没有传入具体币种，使用默认列表
        self.cryptos = cryptos or [
            'BTCUSDT',   # 比特币
            'ETHUSDT',   # 以太坊
            'BNBUSDT',   # BNB
            'ADAUSDT',   # 卡尔达诺
            'SOLUSDT'    # 索拉纳
        ]
    
    def fetch_crypto_data(self, start_date: str, end_date: str, interval: str = Client.KLINE_INTERVAL_1DAY) -> pd.DataFrame:
        """
        获取Binance加密货币历史K线数据
        
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param interval: K线周期
        :return: 加密货币价格DataFrame
        """
        # 存储所有币种数据的字典
        price_data = {}
        
        for symbol in self.cryptos:
            try:
                # 获取K线数据
                klines = self.client.get_historical_klines(
                    symbol, 
                    interval, 
                    start_str=start_date, 
                    end_str=end_date
                )
                
                # 转换为DataFrame
                df = pd.DataFrame(klines, columns=[
                    'open_time', 'open', 'high', 'low', 'close', 
                    'volume', 'close_time', 'quote_asset_volume', 
                    'number_of_trades', 'taker_buy_base_asset_volume', 
                    'taker_buy_quote_asset_volume', 'ignore'
                ])
                
                # 转换时间戳和价格
                df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
                df.set_index('open_time', inplace=True)
                
                # 使用收盘价
                price_data[symbol] = df['close'].astype(float)
                
            except Exception as e:
                print(f"获取 {symbol} 数据时出错: {e}")
        
        # 合并所有币种数据
        return pd.DataFrame(price_data)
    
    def calculate_correlation_matrix(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        计算加密货币间的相关性矩阵
        
        :param data: 加密货币价格DataFrame
        :return: 相关性矩阵
        """
        # 计算日收益率
        returns = data.pct_change()
        
        # 计算皮尔逊相关系数
        correlation_matrix = returns.corr(method='pearson')
        return correlation_matrix
    
    def identify_ecosystem_clusters(self, correlation_matrix: pd.DataFrame, threshold: float = 0.7) -> list:
        """
        识别加密货币生态系统聚类
        
        :param correlation_matrix: 相关性矩阵
        :param threshold: 聚类相关性阈值
        :return: 生态系统聚类列表
        """
        # 创建相关性网络图
        G = nx.Graph()
        
        # 添加节点和边
        for crypto1 in correlation_matrix.index:
            G.add_node(crypto1)
            for crypto2 in correlation_matrix.columns:
                if crypto1 != crypto2:
                    correlation = correlation_matrix.loc[crypto1, crypto2]
                    if correlation >= threshold:
                        G.add_edge(crypto1, crypto2, weight=correlation)
        
        # 使用社区检测算法识别生态系统聚类
        clusters = list(nx.community.greedy_modularity_communities(G))
        
        return clusters
    
    def analyze_ecosystem_dynamics(self, data: pd.DataFrame, reference_crypto: str = 'ETHUSDT'):
        """
        分析加密货币生态系统动态
        
        :param data: 加密货币价格DataFrame
        :param reference_crypto: 参考加密货币
        """
        # 计算相关性矩阵
        correlation_matrix = self.calculate_correlation_matrix(data)
        
        # 识别生态系统聚类
        ecosystem_clusters = self.identify_ecosystem_clusters(correlation_matrix)
        
        # 可视化相关性矩阵
        plt.figure(figsize=(10, 8))
        plt.imshow(correlation_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
        plt.colorbar(label='Correlation')
        plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=45)
        plt.yticks(range(len(correlation_matrix.index)), correlation_matrix.index)
        plt.title(f'Crypto Correlation Matrix')
        plt.tight_layout()
        plt.show()
        
        # 打印分析结果
        print(f"参考加密货币: {reference_crypto}")
        print("\n相关性矩阵:")
        print(correlation_matrix)
        
        print("\n生态系统聚类:")
        for i, cluster in enumerate(ecosystem_clusters, 1):
            print(f"生态系统 {i}: {list(cluster)}")
        
        # 分析参考加密货币的生态系统
        ref_cluster = None
        for cluster in ecosystem_clusters:
            if reference_crypto in cluster:
                ref_cluster = cluster
                break
        
        if ref_cluster:
            print(f"\n{reference_crypto} 所在生态系统:")
            print(list(ref_cluster))
        
        return correlation_matrix, ecosystem_clusters

# 使用示例
if __name__ == "__main__":
    # 注意：如果没有API key和secret，可以传None
    # 对于公共数据，通常不需要身份验证
    analyzer = BinanceCryptoEcosystemAnalyzer(
        # api_key='your_api_key',
        # api_secret='your_api_secret',
        cryptos = [
        "ETHUSDT",        # 主币
        "ENSUSDT",       # 预言机
        "UNIUSDT",       # DEX
        "PEPEUSDT",       # MEMECOIN
        "AAVEUSDT",       # 借贷协议
        "MKRUSDT",        # 稳定币协议
        "CRVUSDT"
        # "POLUSDT"         # Layer2扩容方案
        # "OPUSDT"    # Layer2扩容方案
        # "CRVUSDT"
    ]
    )
    
    # 执行分析
    correlation_matrix, ecosystem_clusters = analyzer.analyze_ecosystem_dynamics(
        analyzer.fetch_crypto_data("2023-01-01", "2024-11-27")
    )