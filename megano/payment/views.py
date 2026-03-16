from django.db import transaction
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from .models import Payment
from .serializers import PaymentSerializer


class PaymentAPIView(APIView):
    def post(self, request: Request, pk: int) -> Response:
        if not request.user.is_authenticated:
            return Response(
                data={"detail": "Требуется авторизация"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        profile = request.user.profile
        order = Order.objects.get(pk=pk, user=profile)

        serializer = PaymentSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        payment_data = serializer.validated_data

        try:
            with transaction.atomic():
                for item in order.items.select_related("product"):
                    product = item.product
                    if product.count < item.count:
                        raise ValueError(
                            f"Недостаточно товара '{product.title}' "
                            f"(нужно {item.count}, в наличии {product.count})"
                        )
                    product.count -= item.count
                    product.save(update_fields=["count"])

                Payment.objects.create(order=order, **payment_data)
        except Exception:
            return Response(
                data={"detail": "Ошибка при обработке платежа"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            data={"detail": "Оплата успешно обработана"},
            status=status.HTTP_200_OK,
        )
