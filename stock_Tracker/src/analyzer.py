from datetime import datetime

class StockAnalyzer:
    def __init__(self, config):
        self.alerts = config.get('alerts', {})

    def check_alerts(self, df):
        alerts = []
        threshold = self.alerts.get('price_change', 3.0)
        for _, row in df.iterrows():
            change = abs(row['涨跌幅'])
            if change >= threshold:
                direction = '大涨' if row['涨跌幅'] > 0 else '大跌'
                alerts.append({
                    'name': row['名称'],
                    'code': row['代码'],
                    'change': row['涨跌幅'],
                    'direction': direction,
                    'price': row['最新价']
                })
        return alerts

    def generate_summary(self, df, news_dict):
        lines = []
        today = datetime.now().strftime('%Y-%m-%d')

        lines.append(f'每日股票简报 —— {today}')
        lines.append('')

        if df.empty:
            lines.append('今日未能获取到行情数据，可能是非交易日或接口异常。')
            return '\n'.join(lines)

        up_count = len(df[df['涨跌幅'] > 0])
        down_count = len(df[df['涨跌幅'] < 0])
        avg_change = df['涨跌幅'].mean()

        lines.append(f'市场总览')
        lines.append(f'  关注股票 {len(df)} 只')
        lines.append(f'  上涨 {up_count} 只 | 下跌 {down_count} 只')
        lines.append(f'  平均涨跌幅: {avg_change:.2f}%')
        lines.append('')

        lines.append('个股行情')
        df_sorted = df.sort_values('涨跌幅', ascending=False)
        for _, row in df_sorted.iterrows():
            arrow = '+' if row['涨跌幅'] > 0 else ''
            lines.append(f"  {row['名称']}({row['代码']}): {row['最新价']:.2f} ({arrow}{row['涨跌幅']:.2f}%)")
        lines.append('')

        top3 = df_sorted.head(3)
        bottom3 = df_sorted.tail(3)
        lines.append('涨幅前三')
        for _, row in top3.iterrows():
            lines.append(f"  + {row['名称']}: {row['涨跌幅']:+.2f}%")
        lines.append('')
        lines.append('跌幅前三')
        for _, row in bottom3.iterrows():
            lines.append(f"  - {row['名称']}: {row['涨跌幅']:+.2f}%")
        lines.append('')

        if news_dict:
            lines.append('最新资讯')
            for name, news_list in news_dict.items():
                if news_list:
                    lines.append(f'\n{name}')
                    for item in news_list[:3]:
                        lines.append(f"  - {item['新闻标题']}")
                else:
                    lines.append(f'\n{name}：暂无最新资讯')
        lines.append('')

        alerts = self.check_alerts(df)
        if alerts:
            lines.append('异常波动提醒')
            for alert in alerts:
                lines.append(f"  {alert['direction']} {alert['name']}({alert['code']}): {alert['change']:+.2f}% 现价 {alert['price']:.2f}")
            lines.append('')

        lines.append('---')
        lines.append(f'报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        lines.append('本报告由 Stock Watcher 自动生成')

        return '\n'.join(lines)
