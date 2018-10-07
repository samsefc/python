#to do
#Book in KDB - iterate through len(book[bid])
#In KDB, create Tickerplant on 5000, RTS on 5001 and Hdb on 5002 - create logging and replaying from logfiles
#the python logfiles are way to big - need to light them(seems way to big compared to binary kdb) 
#ccy pair, adding conversions between the exchanges
#iterate through each ccypairs to create the feeds:
##from cryptofeed.poloniex.pairs import poloniex_trading_pairs
##	poloniex_trading_pairs2 = [w.replace('_', '-') for w in poloniex_trading_pairs]

from cryptofeed.callback import TickerCallback, TradeCallback, BookCallback, FundingCallback
from cryptofeed import FeedHandler
from cryptofeed import Bitmex, Bitfinex, Poloniex, Gemini, HitBTC, Bitstamp
#cryptofeed.Bitfinex
from cryptofeed.defines import L3_BOOK, L2_BOOK, BID, ASK, TRADES, TICKER, FUNDING
import time
from qpython import qconnection
#import qpython
##CCYPAIRS: for future references - might want to do some conversion in the python
from cryptofeed.standards import pair_exchange_to_std, pair_std_to_exchange
from cryptofeed.bitfinex.pairs import bitfinex_trading_pairs
from cryptofeed.gemini.pairs import gemini_trading_pairs
from cryptofeed.hitbtc.pairs import hitbtc_trading_pairs
from cryptofeed.bitstamp.pairs import bitstamp_trading_pairs
#open a q process on port 5002
q = qconnection.QConnection(host='localhost',port = 5002, pandas=True)
q.open()

##Defining KDB Functions and tables:
q.sync("""trade:([]datetime:`datetime$();
        side:`symbol$();
        amount:`float$();
        price:`float$();
        exch:`symbol$())""")
q.sync("""bestprice:([]datetime:`datetime$();
        sym:`symbol$();
        bid:`float$();
        bid_exchange:`symbol$();
        ask:`float$();
        ask_exchange:`symbol$())""")
q.sync("""quote:([]datetime:`datetime$();
        sym:`symbol$();
        bid:`float$();
        ask:`float$();
        exch:())""")
q.sync("""upd:insert""")


async def trade(feed,pair,id,timestamp,side,amount,price):
        localtime = time.time()
        print('feed: {} Pair: {} System Timestamp: {} Amount: {} Price: {} Side: {}'.format(feed, pair, localtime, amount, price, side))
        q.sync('upd[`trade;(.z.z;`{};{};{};`{})]'.format(side,float(amount),float(price),str(feed)))


def nbbo_ticker(pair, bid, ask, bid_feed, ask_feed):
    print('Pair: {} Bid: {} Bid Feed: {} Ask: {} Ask Feed: {}'.format(pair,bid,bid_feed,ask,ask_feed))
    q.sync('upd[`bestprice;(.z.z;`$"{}";{};`{};{};`{})]'.format(str(pair),float(bid),str(bid_feed),float(ask),str(ask_feed)))


async def ticker(feed, pair, bid, ask):
    print('Feed: {} Pair: {} Bid: {} Ask: {}'.format(feed, pair, bid, ask))
    q.sync('upd[`quote;(.z.z;`$"{}";{};{};`{})]'.format(str(pair),float(bid),float(ask),str(feed)))

async def book(feed, pair, book, timestamp):
    print('Timestamp: {} Feed: {} Pair: {} Bid_Size: {} Ask_Size: {}'.format(timestamp, feed, pair, len(book[BID]), len(book[ASK])))
    #q.sync('show (.z.z;`{};{};{};`{})'.format(timestamp, feed, pair, len(book[BID]), len(book[ASK])))


async def funding(**kwargs):
    print("Funding Update for {}".format(kwargs['feed']))
    print(kwargs)

	#debug :  f.last_msg.copy()


	#bitmex_symbols = Bitmex.get_active_symbols()


def main():
	
    f = FeedHandler()
	#BitFinex
    f.add_feed(Bitfinex(pairs=['BTC-USD'], channels=[L2_BOOK, TICKER], callbacks={L2_BOOK: BookCallback(book), TICKER: TickerCallback(ticker)}))
    f.add_feed(Bitfinex(pairs=['BTC-USD'], channels=[TRADES], callbacks={TRADES: TradeCallback(trade)}))
    f.add_nbbo([Bitfinex, Gemini, HitBTC, Bitstamp], ['BTC-USD'], nbbo_ticker)
    f.add_feed(Poloniex(channels=['USDT-BTC', 'USDC-BTC'], callbacks={TICKER: TickerCallback(ticker)}))
    f.add_feed(Poloniex(channels=['USDT-BTC', 'USDC-BTC'], callbacks={L2_BOOK: BookCallback(book)}))
    f.add_feed(Poloniex(channels=['USDT-BTC', 'USDC-BTC'], callbacks={TRADES: TradeCallback(trade)}))
    f.add_feed(Gemini(pairs=['BTC-USD'], callbacks={L2_BOOK: BookCallback(book), TRADES: TradeCallback(trade)}))
    f.add_feed(HitBTC(channels=[TRADES], pairs=['BTC-USD'], callbacks={TRADES: TradeCallback(trade)}))
    f.add_feed(HitBTC(channels=[L2_BOOK], pairs=['BTC-USD'], callbacks={L2_BOOK: BookCallback(book)}))
    f.add_feed(Bitmex(pairs=['XBTUSD'], channels=[TRADES], callbacks={TRADES: TradeCallback(trade)}))
    f.add_feed(Bitmex(pairs=['XBTUSD'], channels=[L3_BOOK], callbacks={L3_BOOK: BookCallback(book)}))
    f.add_feed(Bitstamp(channels=[L2_BOOK, TRADES], pairs=['BTC-USD'], callbacks={L2_BOOK: BookCallback(book), TRADES: TradeCallback(trade)})) 
    #f.add_nbbo([Bitfinex, Gemini], ['BTC-USD'], nbbo_ticker)

    f.add_feed(Bitfinex(pairs=['BTC-USD'], channels=[TICKER], callbacks={TICKER: TickerCallback(ticker)}))
    f.add_feed(Gemini(pairs=['BTC-USD'], callbacks={TICKER: TickerCallback(ticker)}))
    f.add_feed(HitBTC(pairs=['BTC-USD'], channels=[TICKER], callbacks={TICKER: TickerCallback(ticker)}))
    #f.add_feed(Bitmex(Bitstamp=['BTC-USD'], channels=[TICKER], callbacks={TICKER: TickerCallback(ticker)}))
    f.run()
	
if __name__ == '__main__':
    main()
