from rest_framework import viewsets
from .models import Card, CreditAccount, Transaction
from .serializers import (
    CardSerializer,
    CreditAccountSerializer,
    TransactionSerializer
)


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.order_by('-card_number')
    serializer_class = CardSerializer


class CreditAccountViewSet(viewsets.ModelViewSet):
    queryset = CreditAccount.objects.order_by('-account_number')
    serializer_class = CreditAccountSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.order_by('-transaction_date')
    serializer_class = TransactionSerializer
