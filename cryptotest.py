#testing script from Bryant Moscon
'''
Copyright (C) 2017-2018  Bryant Moscon - bmoscon@gmail.com
Please see the LICENSE file for the terms and conditions
associated with this software.
'''
from cryptofeed.callback import TickerCallback, TradeCallback, BookCallback, FundingCallback
from cryptofeed import FeedHandler
from cryptofeed import Bitmex, Bitfinex, Poloniex, Gemini, HitBTC, Bitstamp
from cryptofeed.defines import L3_BOOK, L2_BOOK, BID, ASK, TRADES, TICKER, FUNDING
#from cryptofeed.exchanges import COINBASE



# Examples of some handlers for different updates. These currently don't do much.
# Handlers should conform to the patterns/signatures in callback.py
# Handlers can be normal methods/functions or async. The feedhandler is paused
# while the callbacks are being handled (unless they in turn await other functions or I/O)
# so they should be as lightweight as possible
async def ticker(feed, pair, bid, ask):
    print('Feed: {} Pair: {} Bid: {} Ask: {}'.format(feed, pair, bid, ask))


async def trade(feed, pair, order_id, timestamp, side, amount, price):
    print("Timestamp: {} Feed: {} Pair: {} ID: {} Side: {} Amount: {} Price: {}".format(timestamp, feed, pair, order_id, side, amount, price))

#async def book(feed, pair, book, timestamp):
#    print('Timestamp: {} Feed: {} Pair: {} Bid_Size: {} Ask_Size: {}'.format(timestamp, feed, pair, len(book[BID]), len(book[ASK])))

def nbbo_ticker(pair, bid, ask, bid_feed, ask_feed):
    print('Pair: {} Bid: {} Bid Feed: {} Ask: {} Ask Feed: {}'.format(pair,bid,bid_feed,ask,ask_feed))



async def funding(**kwargs):
    print("Funding Update for {}".format(kwargs['feed']))
    print(kwargs)

from cryptofeed.poloniex.pairs import poloniex_trading_pairs
poloniex_trading_pairs2 = [w.replace('_', '-') for w in poloniex_trading_pairs]



def main():
    f = FeedHandler()
    #for ccypair in poloniex_trading_pairs2:f.add_feed(Poloniex(channels=[ccypair], callbacks={TICKER: TickerCallback(ticker)}))
#working
    #f.add_feed(Bitfinex(pairs=['BTC-USD'], channels=[L2_BOOK, TICKER], callbacks={L2_BOOK: BookCallback(book), TICKER: TickerCallback(ticker)}))
    #f.add_nbbo([Bitfinex, Gemini, HitBTC, Bitstamp], ['BTC-USD'], nbbo_ticker)
    #f.add_feed(Poloniex(channels=['USDT-BTC', 'USDC-BTC','BTC-LSK'], callbacks={TICKER: TickerCallback(ticker)}))
    #f.add_feed(Poloniex(channels=['USDT-BTC', 'USDC-BTC'], callbacks={L2_BOOK: BookCallback(book)}))
    #f.add_feed(Poloniex(channels=['USDT-BTC', 'USDC-BTC'], callbacks={TRADES: TradeCallback(trade)}))
    #f.add_feed(Gemini(pairs=['BTC-USD'], callbacks={L2_BOOK: BookCallback(book), TRADES: TradeCallback(trade)}))
    #f.add_feed(HitBTC(channels=[TRADES], pairs=['BTC-USD'], callbacks={TRADES: TradeCallback(trade)}))
    f.add_feed(HitBTC(channels=[L2_BOOK], pairs=['BTC-USD'], callbacks={L2_BOOK: BookCallback(book)}))
    #f.add_feed(Bitmex(pairs=['XBTUSD'], channels=[FUNDING, TRADES], callbacks={FUNDING: FundingCallback(funding), TRADES: TradeCallback(trade)}))
    #f.add_feed(Bitfinex(pairs=['BTC'], channels=[FUNDING], callbacks={FUNDING: FundingCallback(funding)}))
    #f.add_feed(Bitmex(pairs=['XBTUSD'], channels=[L3_BOOK], callbacks={L3_BOOK: BookCallback(book)}))
    #f.add_feed(Bitstamp(channels=[L2_BOOK, TRADES], pairs=['BTC-USD'], callbacks={L2_BOOK: BookCallback(book), TRADES: TradeCallback(trade)})) 

    f.run()


if __name__ == '__main__':
    main()


