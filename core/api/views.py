from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout, forms, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .forms import RegistrationForm, ProfileEditForm
from .models import Cryptocurrency, Wallet, CryptocurrencyBalance, Transaction, Order, Profile
from .serializers import CryptocurrencySerializer, WalletSerializer, CryptocurrencyBalanceSerializer, TransactionSerializer, OrderSerializer, ProfileSerializer, UserSerializer
from .tasks import send_registration_email

def home(request):
    return render(request, 'home.html', {'user': request.user})


#Authorization
def basic_form(request, given_form):
    if request.method == 'POST':
        form = given_form(data=request.POST)
        if form.is_valid():
            user = form.save()
            send_registration_email.send(user.id)  
            return redirect('login')
        else:
            raise Exception(f"some errors {form.errors}")
    return render(request, 'index.html', {'form': given_form()})

def register_view(request):
    return basic_form(request, RegistrationForm)


def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        form = forms.AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request, user)
                if next_url := request.GET.get("next"):
                    return redirect(next_url)
                return redirect('profile')
            else:
                return HttpResponse("Invalid login")
        else:
            raise Exception(f"some errors {form.errors}")
    return render(request, 'index.html', {'form': forms.AuthenticationForm()})


# ViewSets
class CryptocurrencyViewSet(viewsets.ModelViewSet):
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

class CryptocurrencyBalanceViewSet(viewsets.ModelViewSet):
    queryset = CryptocurrencyBalance.objects.all()
    serializer_class = CryptocurrencyBalanceSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Profiles
@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)

        if 'profile-form' in request.POST and profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
        elif 'password-form' in request.POST and password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, user)  # Updating the session after changing the password
            return redirect('profile')
    else:
        profile_form = ProfileEditForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(request, 'profile.html', {'user': user, 'profile_form': profile_form, 'password_form': password_form})


# Cryptocurrencies
@api_view(['GET'])
def cryptocurrencies_list(request):
    cryptocurrencies = Cryptocurrency.objects.all()
    serializer = CryptocurrencySerializer(cryptocurrencies, many=True)
    return render(request, 'cryptocurrencies_list.html', {'cryptocurrencies': serializer.data})


@api_view(['GET', 'POST'])
def cryptocurrency_detail(request, symbol):
    try:
        cryptocurrency = Cryptocurrency.objects.get(symbol=symbol)
    except Cryptocurrency.DoesNotExist as e:
        return JsonResponse({'message': str(e)}, status=400)

    if request.method == 'POST':
        # Update cryptocurrency price or other details
        form_data = request.POST
        cryptocurrency.current_price = form_data.get('current_price', cryptocurrency.current_price)
        cryptocurrency.save()
        return redirect('cryptocurrency_detail', symbol=symbol)
    
    serializer = CryptocurrencySerializer(cryptocurrency)
    return render(request, 'cryptocurrency_detail.html', {'cryptocurrency': serializer.data})


# Wallets
@login_required
def wallet_view(request):
    wallet = get_object_or_404(Wallet, user=request.user)
    balances = CryptocurrencyBalance.objects.filter(wallet=wallet)
    return render(request, 'wallet.html', {'wallet': wallet, 'balances': balances})


# Transactions
@login_required
@api_view(['GET', 'POST'])
def transaction_list(request):
    if request.method == 'GET':
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        user = request.user
        data = request.data
        cryptocurrency = get_object_or_404(Cryptocurrency, symbol=data['symbol'])
        transaction = Transaction(
            user=user,
            cryptocurrency=cryptocurrency,
            type=data['type'],
            amount=data['amount'],
            price=cryptocurrency.current_price
        )
        transaction.save()
        return Response({'message': 'Transaction created successfully'}, status=status.HTTP_201_CREATED)


# Orders
@login_required
@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        user = request.user
        data = request.data
        cryptocurrency = get_object_or_404(Cryptocurrency, symbol=data['symbol'])
        order = Order(
            user=user,
            cryptocurrency=cryptocurrency,
            type=data['type'],
            amount=data['amount'],
            total_price=cryptocurrency.current_price * data['amount']
        )
        order.save()
        return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)


