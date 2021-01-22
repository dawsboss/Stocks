import math
import numpy as np


class Stock:
    def __init__(self):
        self.ticker = "NONE"            #Ticker of the stock
        self.name = "NONE"              #Name of the company 
        self.numOfShares = 0            #Number of shares you own
        self.buyingPrice = 0            #(Avg) Price stocks bought
        self.price = 0.0                #Price of the stock
        self.precentChange = 0.0        #Daily precent chanage
        self.change = 0.0               #Dollar change value
        self.todayTotalChangePrice = 0  #Change * ShareNum
        self.PE = 0                     #P/E ratio
        self.costBase = 0               #numShares * BuyingPrice
        self.marketValue = 0            #Price * numShares
        self.gainsLosses = 0            #MarketValue - CostBase
        self.growth = 0                 #total growth
        self.dividend = 0.0             #Dividend dollar value
        self.precentDividend = 0.0      #Dividend precent
        self.payoutType = "NONE"        #How often dividends payout
        self.nextPayoutData = "Never"   #Date of the next payout
    
    def updatePrice(self):
        pass
    def updatePrecentChange(self):
        pass
    def updateChange(self):
        pass
    def updatePE(self):
        pass
    def updateCostBase(self):
        self.costBase = self.numOfShares * self.buyingPrice
    def updateMarketValue(self):
        slef.marketValue = self.price * self.nomOfShares
    def updateGainsLosses(self):
        self.gainsLosses = self.marketValue - self.costBase
    def updateGrowth(self):
        self.growth = (self.price - self.buyingPrice)/self.buyingPrice
    def updateDividend(self):
        pass
    def updatePrecentDividend(self):
        pass
    def updatePayoutType(self):
        pass
    def updateNextPayoutDate(Self):
        pass




