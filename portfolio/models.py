import urllib
import json

from django.db import models


class Portfolio(models.Model):
    session = models.CharField(max_length=200, null=True)
    cash_balance = models.IntegerField(null=True)
    
    @classmethod
    def initialize_session(cls, session):
        '''simulate logged in user'''
        portfolio, created = cls.objects.get_or_create(session=session.session_key)
        if created:
            portfolio.cash_balance = 100000
            portfolio.save()
        return portfolio
        
    def get_quote(self, ticker):
        conn = urllib.urlopen("http://data.benzinga.com/stock/%s" % ticker)
        quote = json.loads(conn.read())
        return quote
    
    def get_bid(self, ticker):
        quote = self.get_quote(ticker)
        bid = float(quote['bid'])
        return bid   
    
    def get_ask(self, ticker):
        quote = self.get_quote(ticker)
        bid = float(quote['ask'])
        return bid    
    
    def check_balance(self, price):
        if price < self.cash_balance or price == self.cash_balance:
            return price
        else:
            return False
        
    def process_order(self, order, sell=True):
        ticker = order['ticker']
        units = int(order['units'])
        if not sell:
            ask = self.get_ask(ticker)
            price_or_false = self.check_balance(ask * units)
            if price_or_false:
                #enough cash
                self.cash_balance = self.cash_balance - price_or_false 
                self.save()
                purchase = StockPurchase(portfolio=self, ticker=ticker, units=units, purchase_price=price_or_false)
                
                purchase.save()
                return True
            else:
                #not enough cash
                return False
        else:
            initial_purchase = StockPurchase.objects.get(portfolio=self, pk=order['id'])
            initial_purchase.delete()
            bid = self.get_bid(ticker)
            value = bid * units
            self.cash_balance = self.cash_balance + value
            self.save()
            return True
            
            
class StockPurchase(models.Model):
    portfolio = models.ForeignKey('portfolio.Portfolio')
    ticker = models.CharField(max_length=200)
    units = models.IntegerField()
    purchase_price = models.IntegerField()
    

