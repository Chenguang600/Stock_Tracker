import akshare as ak
import pandas as pd
from datetime import datetime

class StockCollector:
    def __init__(self, watchlist):
        self.watchlist = watchlist

    def get_realtime_prices(self):
        try:
            df = ak.stock_zh_a_spot_em()
            results = []
            for code, name in self.watchlist.items():
                stock = df[df['代码'] == code]
                if not stock.empty:
                    results.append({
                        '代码': code,
                        '名称': name,
                        '最新价': float(stock['最新价'].values[0]),
                        '涨跌幅': float(stock['涨跌幅'].values[0]),
                        '涨跌额': float(stock['涨跌额'].values[0]),
                        '成交量': float(stock['成交量'].values[0]),
                        '成交额': float(stock['成交额'].values[0]),
                    })
            return pd.DataFrame(results)
        except Exception as e:
            print(f'获取行情失败: {e}')
            return pd.DataFrame()

    def get_recent_news(self, stock_name, days=1):
        try:
            df = ak.stock_news_em(symbol=stock_name)
            if df.empty:
                return []
            df['发布时间'] = pd.to_datetime(df['发布时间'])
            today = datetime.now()
            recent = df[df['发布时间'] >= today - pd.Timedelta(days=days)]
            return recent[['发布时间', '新闻标题', '文章来源']].head(5).to_dict('records')
        except:
            return []
