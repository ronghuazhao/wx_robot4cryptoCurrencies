# -*- coding: utf-8 -*-

import asyncio
import os
import sys
from pprint import pprint
import json
from wxpy import * 
#root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#sys.path.append(root + '/python')
#import ccxt.async_support as ccxt  # noqa: E402

import ccxt
import time
from datetime import datetime
import pytz

def timelocal():
    tz = pytz.timezone('Asia/Shanghai') #东八区
    t = datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S %Z%z')
    return t
#exchange_found  = id in ccxt.exchanges
#exchange = getattr(ccxt,id)({
#	# 'proxy':'https://cors-anywhere.herokuapp.com/',
#})
#markets = exchange.load_markets()
#tuples = list(ccxt.Exchange.keysort(markets).items)
#
#for (k,v) in tuples:
#	print(v['symbol'])
#获取所有的交易所， 137个
exchanges = {}
for id in ccxt.exchanges:
	exchange = getattr(ccxt,id)
	exchanges[id] = exchange()
print(exchanges)
def log(*args):
    print(' '.join([str(arg) for arg in args]))

sorted_exchanges = sorted(list(exchanges.keys()))

header_ex = ['binance','okex3','huobipro','coinbase','fcoin','kucoin','kraken','poloniex','upbit','zb','hitbtc','bitfinex','bitz','bitmex','bibox','gateio','bittrex','coss','theocean','coinegg']

other_ex = list(set(sorted_exchanges).difference(set(header_ex)))
#print("other_ex{0}".format(other_ex))
#print("header_ex{0}".format(header_ex))
header_ex.extend(other_ex)
#print("all_ex{0}".format(header_ex))
def search_symbol_in_header_exchange(symbol):
	for exid in header_ex:
		print("exid@search_symbol_in_header_exchange{0}".format(exid))
		symbol_u = symbol.upper() + '/USDT'
		exchange = getattr(ccxt, exid)(
		#{'proxy':'https://cors-anywhere.herokuapp.com/',}
		)
		exchange.has['fetchCurrencies'] = False
		markets = exchange.load_markets()
		try:
			B =  ('.' not in symbol_u) and (('active' not in exchange.markets[symbol_u]) or (exchange.markets[symbol_u]['active']))
			if B == True:
				return {symbol: exid}
		except KeyError:
			pass
		else:
				return None 
def search_symbol_in_other_exchange(symbol):
	for idex in  other_ex:
		exchange = getattr(ccxt, idex)(
		#{'proxy':'https://cors-anywhere.herokuapp.com/',}
		)
		symbol_u = symbol.upper() + '/USDT'
		markets = exchange.load_markets()
		try:
			B =  ('.' not in symbol_u) and (('active' not in exchange.markets[symbol_u]) or (exchange.markets[symbol_u]['active']))
			if B == True:
				return {symbol: idex}
		except KeyError:
			pass
	


def is_active_symbol(exchange, symbol):
    return ('.' not in symbol) and (('active' not in exchange.markets[symbol]) or (exchange.markets[symbol]['active']))


#from chatterbot import ChatBot
#from chatterbot.trainers import ChatterBotCorpusTrainer
#chatbot = ChatBot("deepThought")# 用于回复消息的机器人
#chatbot.set_trainer(ChatterBotCorpusTrainer)
#chatbot.train("chatterbot.corpus.chinese")# 使用该库的中文语料库
#bot = Bot(console_qr=True,cache_path=True)# 用于接入微信的机器人

bot = Bot(console_qr=True, cache_path=True)# 用于接入微信的机器人
Group = bot.groups()# 进行测试的群
bot.enable_puid()
#group_baba = bot.groups().search("BaBa")[0]
#group_baba2 = bot.groups().search("征战新纪元。怀挺！")[0]
    #print(msg.text,msg.type)
    #print("final_msg:{0} ".format(final_msg))
    #print("Group.puid:{0} ".format(msg.chat))
@bot.register(Group,TEXT,run_async=True)
def reply_g_i(msg):
    if msg.text.isalpha():
    	final_msg = get_data(msg.text)
    	print("final_msg:{0} ".format(final_msg))
    	msg.chat.send(final_msg)
    else:pass

#async def sym(id, symbol):
#    print("symbol_@test: {}".format(symbol))
#    exchange = getattr(ccxt, id)({
#        'enableRateLimit': True,  # required according to the Manual
#    })
#    ticker = await exchange.fetch_ticker(symbol)
#    await exchange.close()
#    return ticker
def sym(id, symbol):
    #print("symbol_@test: {}".format(symbol))
    exchange = getattr(ccxt, id)({
        'enableRateLimit': True,  # required according to the Manual
    })
    ticker =  exchange.fetch_ticker(symbol)
    #exchange.close()
    print(ticker)
    return ticker

def get_data_ex(symbol):
    dictvalue = search_symbol_in_header_exchange(symbol)
    if isinstance(dictvalue, dict):
       exid = dictvalue.get(symbol)
       return exid
    else:
       dictothervalue = search_symbol_in_other_exchange(symbol)
       if isinstance(dictothervalue, dict):
          otherexid = dictothervalue.get(symbol)
          return otherexid
       else:pass
def get_data(symbol):
    print("symbol@get_data:{0}".format(symbol))
    #返回交易所id
    exid = get_data_ex(symbol)
    print("exid@get_data:{0}".format(exid))
    symbol_u = symbol.upper() + '/USDT'
    s = sym(exid, symbol_u)
    print("sym@get_data:{0}".format(s))
    data = json.loads(json.dumps(s))
    datetime =timelocal() 
    msg = "交易所:" + exid + " "+ "\n" + " " +  "时间:" + str(datetime) +"\n" +"交易对:" + symbol_u + "\n" +  "最新价格:" + str(data["last"]) + " " +  "\n" + " " + "涨幅:" + str(data["percentage"]) + "%" + " "+ "\n"+ " " + "开盘:" + str(data["open"]) + " " +  "\n" + " " + "最低:" + str(data["low"])  + " " + "\n"+ " " + "最高:" + str(data["high"])   
    return msg
	#msg = "交易所:" + id + "\n" +  "时间:" + data["datetime"] + "\n" +  "最新价格:" + data["last"] + "\n" + "涨幅:" + data["percentage"] + "\n" + "开盘:" + data["open"] + "\n" + "最低:" + data["low"]  + "\n" + "最低:" + data["low"]
embed(shell=None)
#bot.join()
