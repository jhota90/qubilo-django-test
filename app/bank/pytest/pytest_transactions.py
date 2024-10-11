import pytest

from datetime import date
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Card, CreditAccount, Transaction


@pytest.mark.django_db
class TestCard:

    transaction_url = "/api/transactions/"
    transaction_json_data = {
        "amount": "200.00",
        "transaction_date": "2024-10-10",
        "card": None,
    }
    transaction_data = {
        "amount": "200.00",
        "transaction_date": "2024-10-10",
        "card_id": None,
    }

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def card(self):
        credit_account = CreditAccount.objects.create(
            account_number="1234567890",
            balance=1000.00,
            credit_limit=500.00,
        )
        return Card.objects.create(
            card_number="CARD123456789",
            expiration_date=date(2025, 12, 31),
            credit_account=credit_account,
        )

    def test_create_transaction(self, api_client, card):
        self.transaction_json_data["card"] = card.id
        print(self.transaction_json_data)
        response = api_client.post(
            self.transaction_url, self.transaction_json_data, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Transaction.objects.count() == 1

    def test_get_transaction(self, api_client, card):
        self.transaction_data["card_id"] = card.id
        transaction = Transaction.objects.create(**self.transaction_data)
        response = api_client.get(
            f"{self.transaction_url}{transaction.transaction_id}/"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["transaction_id"] == str(transaction.transaction_id)

    def test_update_transaction(self, api_client, card):
        self.transaction_data["card_id"] = card.id
        transaction = Transaction.objects.create(**self.transaction_data)
        update_data = {"transaction_date": "2025-01-01"}
        response = api_client.patch(
            f"{self.transaction_url}{transaction.transaction_id}/",
            update_data,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
            Transaction.objects.get(
                transaction_id=transaction.transaction_id
            ).transaction_date.strftime("%Y-%m-%d")
            == "2025-01-01"
        )

    def test_retrieve_transaction(self, api_client, card):
        self.transaction_data["card_id"] = card.id
        Transaction.objects.create(**self.transaction_data)
        response = api_client.get(self.transaction_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get("results")) == 1

    def test_delete_transaction(self, api_client, card):
        self.transaction_data["card_id"] = card.id
        transaction = Transaction.objects.create(**self.transaction_data)
        response = api_client.delete(
            f"{self.transaction_url}{transaction.transaction_id}/"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Transaction.objects.count() == 0
