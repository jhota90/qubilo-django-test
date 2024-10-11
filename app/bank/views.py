from rest_framework import viewsets
from .models import Card, CreditAccount, Transaction
from .serializers import (
    CardSerializer,
    CreditAccountSerializer,
    TransactionSerializer
)


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CreditAccountViewSet(viewsets.ModelViewSet):
    queryset = CreditAccount.objects.all()
    serializer_class = CreditAccountSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
