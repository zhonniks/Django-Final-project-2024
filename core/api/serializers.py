from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cryptocurrency, Wallet, CryptocurrencyBalance, Transaction, Order, Profile

class CryptocurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class CryptocurrencyBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptocurrencyBalance
        fields = '__all__'
        read_only_fields = ['wallet', 'cryptocurrency']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user', 'timestamp']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['total_price', 'created_at']

    def create(self, validated_data):
        cryptocurrency = validated_data['cryptocurrency']
        amount = validated_data['amount']
        price = cryptocurrency.current_price
        total_price = amount * price
        validated_data['total_price'] = total_price

        return super(OrderSerializer, self).create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
