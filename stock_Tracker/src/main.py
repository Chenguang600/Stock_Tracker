import yaml
from collector import StockCollector
from analyzer import StockAnalyzer
from notifier import EmailNotifier
from datetime import datetime

def main():
    print('股票简报生成工具启动...')

    with open('config/stocks.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    watchlist = config['watchlist']

    collector = StockCollector(watchlist)
    print('正在获取行情数据...')
    df = collector.get_realtime_prices()

    if df.empty:
        print('未获取到行情数据，可能非交易日')
        content = f'股票简报 —— {datetime.now().strftime("%Y-%m-%d")}\n\n今日未能获取到行情数据，可能是非交易日或接口异常。'
        notifier = EmailNotifier()
        notifier.send(f'股票简报 {datetime.now().strftime("%Y-%m-%d")}', content)
        return

    print(f'获取到 {len(df)} 只股票数据')

    print('正在获取相关新闻...')
    news_dict = {}
    for code, name in watchlist.items():
        print(f'  获取 {name} 的新闻...')
        news = collector.get_recent_news(name)
        news_dict[name] = news
        print(f'  找到 {len(news)} 条')

    print('正在分析数据...')
    analyzer = StockAnalyzer(config)
    summary = analyzer.generate_summary(df, news_dict)

    print('正在发送邮件...')
    notifier = EmailNotifier()
    today = datetime.now().strftime('%Y-%m-%d')
    success = notifier.send(f'股票简报 {today}', summary)

    if success:
        print('全部完成！请查收邮件。')
    else:
        print('发送失败，请检查配置。')

if __name__ == '__main__':
    main()
