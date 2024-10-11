from rest_framework import status
from rest_framework.test import APITestCase
from ..models import CreditAccount


class CreditAccountTests(APITestCase):
    def setUp(self):
        self.credit_accounts_url = "/api/credit-accounts/"
        self.account_data = {
            "account_number": "1234567890",
            "balance": 100.00,
            "credit_limit": 500.00,
        }

    def test_create_credit_account(self):
        response = self.client.post(
            self.credit_accounts_url, self.account_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CreditAccount.objects.count(), 1)
        self.assertEqual(CreditAccount.objects.get().account_number, "1234567890")

    def test_get_credit_account(self):
        account = CreditAccount.objects.create(**self.account_data)
        response = self.client.get(f"{self.credit_accounts_url}{account.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["account_number"], account.account_number)

    def test_update_credit_account(self):
        account = CreditAccount.objects.create(**self.account_data)
        update_data = {"balance": 200.00}
        response = self.client.patch(
            f"{self.credit_accounts_url}{account.id}/", update_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CreditAccount.objects.get(id=account.id).balance, 200.00)

    def test_delete_credit_account(self):
        account = CreditAccount.objects.create(**self.account_data)
        response = self.client.delete(f"{self.credit_accounts_url}{account.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CreditAccount.objects.count(), 0)
