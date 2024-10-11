from datetime import date
from decimal import Decimal
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Card, CreditAccount, Transaction


class TransactionAPITest(APITestCase):
    def setUp(self):
        self.transaction_url = "/api/transactions/"
        self.credit_account = CreditAccount.objects.create(
            account_number="1234567890",
            balance=Decimal("1000.00"),
            credit_limit=Decimal("500.00"),
        )
        self.card = Card.objects.create(
            card_number="CARD123456789",
            expiration_date=date(2025, 12, 31),
            credit_account=self.credit_account,
        )
        self.transaction = Transaction.objects.create(
            amount=Decimal("100.00"), transaction_date=date.today(), card=self.card
        )

    def test_create_transaction(self):
        data = {
            "amount": "200.00",
            "transaction_date": str(date.today()),
            "card": self.card.id,
        }
        response = self.client.post(self.transaction_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_transactions(self):
        response = self.client.get(self.transaction_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)
