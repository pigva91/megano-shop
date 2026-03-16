from django.urls import path

from orders.views import OrderAPIView, OrderDetailAPIView
from payment.views import PaymentAPIView

app_name = "payment"

urlpatterns = [
    path("payment/<int:pk>", PaymentAPIView.as_view(), name="payment"),
]
