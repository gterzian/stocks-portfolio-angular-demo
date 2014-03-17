from django.contrib import admin
from django.contrib.sessions.models import Session



from portfolio.models import StockPurchase, Portfolio

admin.site.register(StockPurchase)
admin.site.register(Portfolio)
admin.site.register(Session)


