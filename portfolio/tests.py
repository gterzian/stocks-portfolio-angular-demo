import json
from django.test import TestCase
from portfolio.models import Portfolio
from django.test.client import RequestFactory
from django.contrib.sessions.backends.db import SessionStore

from portfolio.views import new_transaction, get_user

class PortfolioTestCase(TestCase):
    def setUp(self):
        self.pf = Portfolio.objects.create(session='test', cash_balance=100000)
    
    def test_check_balance(self):
        self.assertFalse(self.pf.check_balance(100000000))
        self.assertTrue(self.pf.check_balance(100))
    

class ViewsTestCase(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_getuser(self):
        
        request = self.factory.get('user/')
        request.session = SessionStore()
        request.session.create()
        response = get_user(request)
        self.assertEqual(response.status_code, 200)
        
    
    def test_new_stockpurchase(self):
        request = self.factory.post('new_transaction/', dict(ticker='AM', units=10, sell=True))
        request.session = SessionStore()
        request.session.create()
        response = new_transaction(request)
        self.assertEqual(response.status_code, 200)
    
        
        
