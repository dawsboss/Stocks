import pandas as pd
import numpy as np
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import robin_stocks.robinhood as r
import yfinance as yf #Yahoo historical data


#u = robinhood username
#p = password for robinhood account
#mfa = mfa from robinhood if 2 auth factor active
#api = api for finnhub
class Stocks:
    def __init__(self, u="", p="", mfa=""):
        self.login = r.login(u, p, mfa_code=mfa)
        self.tickers = []
        self.empty=True
        self.all_update()

                
        if self.empty:
            return
        
        
    def all_update(self):
        self.robinhood_update()
        self.yahoo_update()
        
    def live_update(self, sym, time, inter):
        return yf.download(sym, period=time, interval=inter, prepost=False, threads=True)
        
    def yahoo_update(self):
        self.yTicker = {}
        for i in self.tickers:
            self.yTicker[i] = yf.Ticker(i)   
        
    def robinhood_update(self):#Frequent running
        prevtickers = self.tickers.sort()
        
        self._base_update_from_robinhood()

        if self.tickers == []:
            self.empty=True
            return
        
        self._adv_update_from_robinhood()
        
        self.empty=False
        #Simple data per stack
        self.quantities = [float(item["quantity"]) for item in self.positions]
        self.boughtAt = [float(item["average_buy_price"]) for item in self.positions]

        self.prevClose = [float(item["previous_close"]) for item in self.tickerInfo]
        self.lastPrice = [float(item["last_trade_price"]) for item in self.tickerInfo]
        self.bidPrice = [float(item["bid_price"]) for item in self.tickerInfo]
        self.askPrice = [float(item["ask_price"]) for item in self.tickerInfo]
        #
        

        #
        
        self._update_daily_stats()
        self._update_total_stats()






    def _base_update_from_robinhood(self):#Information that doesn't need anything else to retrieve
        self.positions = r.get_open_stock_positions()# Per stock | not clean info
        self.profile_info = r.build_user_profile()# Basic Account info
        self.stock_info = r.build_holdings()# Per stock | clean information USEFUL
        self.upcoming_dividends = r.get_dividends() #Upcoming dicidends
        self.tickers = [r.get_symbol_by_url(item["instrument"]) for item in self.positions]# tickers owned
        self.profileData = r.load_portfolio_profile()# Profile info
        self.allTransactions = r.get_bank_transfers()
        self.cardTransactions= r.get_card_transactions()
        self.dividends = r.get_total_dividends()
        
    def _adv_update_from_robinhood(self):#Info from robinhood but needs other info
        self.get_latest_price= r.get_latest_price(self.tickers)#Lastest Price | Have updateable function
        self.get_fundamentals = r.get_fundamentals(self.tickers)# USEFUL Per Stock | Basic infomation about the comapny
        self.tickerInfo =  r.get_quotes(self.tickers)# Per stock | not clean info



        
        
        
        
    def _update_daily_stats(self):#Not needed frequently updated
        #Daily calculations
        self.dailyProfitPerShare = [float(self.lastPrice[i]) - float(self.prevClose[i]) for i in range(len(self.tickers))]
        self.dailyPercentChange = [ 100.0 * self.dailyProfitPerShare[i] / float(self.prevClose[i]) for i in range(len(self.tickers)) ]
        self.dailyProfit = [self.dailyProfitPerShare[i] * self.quantities[i] for i in range(len(self.tickers))]
    
    def _update_total_stats(self):#Not needed frequently updated
        self.deposits = sum(float(x['amount']) for x in self.allTransactions if (x['direction'] == 'deposit') and (x['state'] == 'completed'))
        self.withdrawals = sum(float(x['amount']) for x in self.allTransactions if (x['direction'] == 'withdraw') and (x['state'] == 'completed'))
        self.debits = sum(float(x['amount']['amount']) for x in self.cardTransactions if (x['direction'] == 'debit' and (x['transaction_type'] == 'settled')))
        self.reversal_fees = sum(float(x['fees']) for x in self.allTransactions if (x['direction'] == 'deposit') and (x['state'] == 'reversed'))

        self.money_invested = self.deposits + self.reversal_fees - (self.withdrawals - self.debits)
        self.percentDividend = self.dividends/self.money_invested*100

        self.equity = float(self.profileData['equity'])
        self.totalGainMinusDividends = self.equity - self.dividends - self.money_invested
        self.percentGain = self.totalGainMinusDividends/self.money_invested*100
        
        
        
    def printDailyInfo(self):
        self._update_daily_stats()
        self.dailyTickersPerf = list(zip(self.dailyProfit, self.dailyPercentChange, self.tickers))
        self.dailyTickersPerf.sort(reverse=True)
        print ("My Positions Performance:")
        print ("Ticker | DailyGain | PercentChange")
        for item in self.dailyTickersPerf:
          print ("%s %f$ %f%%" % (item[2], item[0], item[1]))

        print ("Net Gain:", sum(self.dailyProfit)) 
        
        
    
    def logout(self):
        r.logout()