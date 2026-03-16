from django.urls import path

from orders.views import OrderAPIView, OrderDetailAPIView


app_name = "orders"

urlpatterns = [
    path("orders/", OrderAPIView.as_view(), name="orders-list-create"),
    path("order/<int:pk>", OrderDetailAPIView.as_view(), name="order-detail"),
    path(
        "orders/<int:pk>", OrderDetailAPIView.as_view(), name="orders-detail"
    ),
]
