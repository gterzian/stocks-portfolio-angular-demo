import json

from django.shortcuts import render
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt

from portfolio.models import Portfolio

'''Front End app lives at static/js/controllers.js'''

def index(request):
    context = dict()
    return render(request, 'portfolio/index.html', context)


def get_user(request):
    '''used by front end app to get initial data on page load'''
    session = request.session
    portfolio = Portfolio.initialize_session(session)
    return HttpResponse(json.dumps(dict(cash_balance=portfolio.cash_balance, 
                                        id=portfolio.pk, 
                                        purchases=[dict(ticker=p.ticker, units=p.units, purchase_price=p.purchase_price, id=p.pk) for p in portfolio.stockpurchase_set.all()])))
  
@csrf_exempt    
def new_transaction(request):
    '''used by front end app to send both BUY and SELL orders'''
    if request.method == 'POST':
        try:
            order = json.loads(request.body)
        except ValueError:
            order = request.POST
        portfolio = Portfolio.initialize_session(request.session)
        order = portfolio.process_order(order, True if order['type'] == 'sell' else False) 
        return HttpResponse(json.dumps(dict(success=order,
                                        cash_balance=portfolio.cash_balance, 
                                        id=portfolio.pk, 
                                        purchases=[dict(ticker=p.ticker, units=p.units, purchase_price=p.purchase_price, id=p.pk) for p in portfolio.stockpurchase_set.all()])))
    else:
        return HttpResponse('Sorry post only')

