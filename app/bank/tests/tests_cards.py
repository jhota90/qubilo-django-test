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
        self.card_json_data = {
            "card_number": "CARD987654321",
            "expiration_date": "2024-12-31",
            "credit_account": self.credit_account.id,
        }
        self.card_data = {
            "card_number": "CARD987654321",
            "expiration_date": "2024-12-31",
            "credit_account_id": self.credit_account.id,
        }

    def test_create_card(self):
        response = self.client.post(self.card_url, self.card_json_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_credit_account(self):
        card = Card.objects.create(**self.card_data)
        response = self.client.get(f"{self.card_url}{card.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["card_number"], card.card_number)

    def test_update_credit_account(self):
        card = Card.objects.create(**self.card_data)
        update_data = {"expiration_date": "2025-01-01"}
        response = self.client.patch(
            f"{self.card_url}{card.id}/", update_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Card.objects.get(id=card.id).expiration_date.strftime("%Y-%m-%d"),
            "2025-01-01",
        )

    def test_retrieve_cards(self):
        Card.objects.create(**self.card_data)
        response = self.client.get(self.card_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)

    def test_delete_credit_account(self):
        card = Card.objects.create(**self.card_data)
        response = self.client.delete(f"{self.card_url}{card.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Card.objects.count(), 0)
