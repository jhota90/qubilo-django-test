import pytest
from rest_framework import status
from rest_framework.test import APIClient
from ..models import CreditAccount


@pytest.mark.django_db
class TestCreditAccount:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def credit_account(self):
        return CreditAccount.objects.create(
            account_number="1234567890", balance=100.00, credit_limit=500.00
        )

    def test_create_credit_account(self, api_client):
        account_data = {
            "account_number": "0987654321",
            "balance": 200.00,
            "credit_limit": 600.00,
        }
        response = api_client.post("/api/credit-accounts/", account_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert CreditAccount.objects.count() == 1
        assert CreditAccount.objects.get().account_number == "0987654321"

    def test_get_credit_account(self, api_client, credit_account):
        response = api_client.get(f"/api/credit-accounts/{credit_account.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["account_number"] == credit_account.account_number

    def test_update_credit_account(self, api_client, credit_account):
        update_data = {"balance": 300.00}
        response = api_client.patch(
            f"/api/credit-accounts/{credit_account.id}/", update_data, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert CreditAccount.objects.get(id=credit_account.id).balance == 300.00

    def test_delete_credit_account(self, api_client, credit_account):
        response = api_client.delete(f"/api/credit-accounts/{credit_account.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert CreditAccount.objects.count() == 0
