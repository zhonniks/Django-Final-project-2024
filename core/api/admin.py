from django.contrib import admin

from .models import Cryptocurrency, Wallet, CryptocurrencyBalance, Transaction, Order, Profile

admin.site.register(Cryptocurrency)
admin.site.register(Wallet)
admin.site.register(CryptocurrencyBalance)
admin.site.register(Transaction)
admin.site.register(Order)
admin.site.register(Profile)

