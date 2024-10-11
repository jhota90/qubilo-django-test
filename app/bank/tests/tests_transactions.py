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
        self.transaction_json_data = {
            "amount": "200.00",
            "transaction_date": str(date.today()),
            "card": self.card.id,
        }
        self.transaction_data = {
            "amount": "200.00",
            "transaction_date": str(date.today()),
            "card_id": self.card.id,
        }

    def test_create_transaction(self):
        response = self.client.post(
            self.transaction_url, self.transaction_json_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_transaction(self):
        transaction = Transaction.objects.create(**self.transaction_data)
        response = self.client.get(
            f"{self.transaction_url}{transaction.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["id"], str(transaction.id)
        )

    def test_update_transaction(self):
        transaction = Transaction.objects.create(**self.transaction_data)
        update_data = {"transaction_date": "2025-01-01"}
        response = self.client.patch(
            f"{self.transaction_url}{transaction.id}/",
            update_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Transaction.objects.get(
                id=transaction.id
            ).transaction_date.strftime("%Y-%m-%d"),
            "2025-01-01",
        )

    def test_retrieve_transactions(self):
        Transaction.objects.create(**self.transaction_data)
        response = self.client.get(self.transaction_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)

    def test_delete_credit_account(self):
        transaction = Transaction.objects.create(**self.transaction_data)
        response = self.client.delete(
            f"{self.transaction_url}{transaction.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 0)
