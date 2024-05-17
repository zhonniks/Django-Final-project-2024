from django.urls import path

from rest_framework import routers
from .views import (
    CryptocurrencyViewSet, WalletViewSet, CryptocurrencyBalanceViewSet, 
    TransactionViewSet, OrderViewSet, ProfileViewSet, UserViewSet,
    cryptocurrencies_list, cryptocurrency_detail, wallet_view, 
    transaction_list, order_list, home, register_view, logout_view, 
    login_view, profile
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'cryptocurrencies', CryptocurrencyViewSet)
router.register(r'wallets', WalletViewSet)
router.register(r'cryptocurrency_balances', CryptocurrencyBalanceViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'user_profiles', ProfileViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', home, name='home'),
    path('cryptocurrencies/', cryptocurrencies_list, name='cryptocurrencies_list'),
    path('cryptocurrencies/<str:symbol>/', cryptocurrency_detail, name='cryptocurrency_detail'),
    path('wallet/', wallet_view, name='wallet_view'),
    path('transactions/', transaction_list, name='transaction_list'),
    path('orders/', order_list, name='order_list'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
]

urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
