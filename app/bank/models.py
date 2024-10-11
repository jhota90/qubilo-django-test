from django.db import models
from uuid import uuid4


class CreditAccount(models.Model):
    account_number = models.CharField(
        verbose_name="Account number",
        max_length=20,
        null=False,
        blank=False,
        unique=True
    )
    balance = models.DecimalField(
        verbose_name="Balance",
        decimal_places=2,
        max_digits=17,
        default=0,
        blank=True
    )
    credit_limit = models.DecimalField(
        verbose_name="Credit Limit",
        decimal_places=2,
        max_digits=17,
        default=0,
        blank=True,
    )


class Card(models.Model):
    card_number = models.CharField(
        verbose_name="Card number",
        max_length=50,
        null=False,
        blank=True,
        unique=True
    )
    expiration_date = models.DateField(
        verbose_name="Expiration date",
        null=False,
        blank=False
    )
    credit_account = models.ForeignKey(
        to=CreditAccount,
        on_delete=models.DO_NOTHING,
        verbose_name="Credit account",
        null=False,
        blank=False
    )


class Transaction(models.Model):
    id = models.UUIDField(
        primary_key=True,
        verbose_name="Transaction ID",
        default=uuid4
    )
    amount = models.DecimalField(
        verbose_name="Amount",
        decimal_places=2,
        max_digits=17,
        default=0,
        blank=True,
    )
    transaction_date = models.DateField(
        verbose_name="Transaction date",
        null=False,
        blank=False,
        db_index=True
    )
    card = models.ForeignKey(
        to=Card,
        on_delete=models.DO_NOTHING,
        verbose_name="Card",
        null=False,
        blank=False
    )
