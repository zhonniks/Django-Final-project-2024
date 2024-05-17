from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Cryptocurrency, Wallet, CryptocurrencyBalance, Transaction, Order, Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class CryptocurrencyForm(forms.ModelForm):
    class Meta:
        model = Cryptocurrency
        fields = ['name', 'symbol', 'current_price']


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['balance']


class CryptocurrencyBalanceForm(forms.ModelForm):
    class Meta:
        model = CryptocurrencyBalance
        fields = ['amount']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['cryptocurrency', 'type', 'amount', 'price']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['cryptocurrency', 'type', 'amount']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date']
