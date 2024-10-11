from datetime import date
from decimal import Decimal
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import CreditAccount, Card


class CardAPITest(APITestCase):
    def setUp(self):
        self.card_url = "/api/cards/"
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

    def test_create_card(self):
        data = {
            "card_number": "CARD987654321",
            "expiration_date": "2026-12-31",
            "credit_account": self.credit_account.id,
        }
        response = self.client.post(self.card_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_cards(self):
        response = self.client.get(self.card_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)
