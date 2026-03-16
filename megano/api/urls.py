from django.urls import path, include


urlpatterns = [
    path("", include("profiles.urls")),
    path("", include("catalog.urls")),
    path("", include("basket.urls")),
    path("", include("orders.urls")),
    path("", include("payment.urls")),
]
