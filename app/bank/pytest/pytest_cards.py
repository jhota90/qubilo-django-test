import pytest
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Card, CreditAccount


@pytest.mark.django_db
class TestCard:

    cards_url = "/api/cards/"
    card_json_data = {
        "card_number": "CARD987654321",
        "expiration_date": "2024-12-31",
        "credit_account": None,
    }
    card_data = {
        "card_number": "CARD987654321",
        "expiration_date": "2024-12-31",
        "credit_account_id": None,
    }

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def credit_account(self):
        return CreditAccount.objects.create(
            account_number="1234567890", balance=100.00, credit_limit=500.00
        )

    def test_create_card(self, api_client, credit_account):
        self.card_json_data["credit_account"] = credit_account.id
        response = api_client.post(self.cards_url, self.card_json_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Card.objects.count() == 1
        assert Card.objects.get().card_number == self.card_data.get("card_number")

    def test_get_card(self, api_client, credit_account):
        self.card_data["credit_account_id"] = credit_account.id
        card = Card.objects.create(**self.card_data)
        response = api_client.get(f"{self.cards_url}{card.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["card_number"] == card.card_number

    def test_update_card(self, api_client, credit_account):
        self.card_data["credit_account_id"] = credit_account.id
        card = Card.objects.create(**self.card_data)
        update_data = {"expiration_date": "2025-01-01"}
        response = api_client.patch(
            f"{self.cards_url}{card.id}/",
            update_data,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
            Card.objects.get(id=card.id).expiration_date.strftime("%Y-%m-%d")
            == "2025-01-01"
        )

    def test_retrieve_card(self, api_client, credit_account):
        self.card_data["credit_account_id"] = credit_account.id
        Card.objects.create(**self.card_data)
        response = api_client.get(self.cards_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get("results")) == 1

    def test_delete_card(self, api_client, credit_account):
        self.card_data["credit_account_id"] = credit_account.id
        card = Card.objects.create(**self.card_data)
        response = api_client.delete(f"{self.cards_url}{card.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Card.objects.count() == 0
