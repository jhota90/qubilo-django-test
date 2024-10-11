from django.urls import include, path
from rest_framework import routers
from .views import CardViewSet, CreditAccountViewSet, TransactionViewSet

router = routers.DefaultRouter()
router.register(r'credit-accounts', CreditAccountViewSet)
router.register(r'cards', CardViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
