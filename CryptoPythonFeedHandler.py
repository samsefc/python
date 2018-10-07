from cryptofeed.callback import TradeCallback
from cryptofeed import FeedHandler
from cryptofeed import Bitmex,Bitstamp,Bitfinex, GDAX
from cryptofeed.defines import TRADES
import time
#from qpython import qconnection
import qpython

q = qconnection.QConnection(host='localhost',port = 5002, pandas=True)
q.open()

q.sync("""trade:([]systemtime:`datetime$();
        side:`symbol$();
        amount:`float$();
        price:`float$();
        exch:`symbol$())""")

async def trade(feed,pair,id,timestamp,side,amount,price):
        locatime = time.time()
        print('feed: {} Pair: {} System Timestamp: {} Amount: {} Price: {} Side: {}'.format(
            feed, pair, localtime, amount, price, side,
            ))
        q.sync('`trade insert (.z.z;`{};`{}`{}`{})'.format(
            side,
            float(amount),
            float(price),
            str(feed)
        ))
        
def main():
    f = FeedHandler()
    f.add_feed(Bitmex(pairs=['XBTUSD'], channels=[TRADES], callbacks={TRADES:TradeCallback(trade)}))
    f.run
    
if __name__ == '__main__':
    main()