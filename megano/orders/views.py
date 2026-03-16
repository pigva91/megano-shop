from basket.basket_session import BASKET_SESSION_KEY, get_basket
from basket.models import Basket
from basket.serializers import BasketItemSerializer
from orders.models import Order, OrderItem
from orders.serializers import (
    OrderCreateSerializer,
    OrderIdResponseSerializer,
    OrderSerializer,
)
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import Optional


class OrderAPIView(APIView):
    def get(self, request: Request) -> Response:
        if request.user.is_authenticated:
            orders = (
                Order.objects.filter(user=request.user.profile)
                .select_related("user")
                .prefetch_related("items__product")
            )
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)

        basket_items = get_basket(request)
        if not basket_items:
            return Response(
                data={"detail": "Корзина пуста"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total_cost = sum(
            item["product"].price * item["count"] for item in basket_items
        )
        basket_items_serializer = BasketItemSerializer(basket_items, many=True)
        products_data = basket_items_serializer.data
        fake_order_data = {
            "id": None,
            "createdAt": None,
            "fullName": "",
            "email": "",
            "phone": "",
            "deliveryType": "",
            "paymentType": "",
            "totalCost": float(total_cost),
            "status": "",
            "city": "",
            "address": "",
            "products": products_data,
        }
        return Response(fake_order_data)

    def post(self, request: Request) -> Response:
        basket_items = get_basket(request)

        if request.user.is_authenticated:
            profile = request.user.profile
            full_name = profile.fullName
            email = profile.email
            phone = profile.phone
        else:
            full_name = ""
            email = ""
            phone = ""

        order = Order.objects.create(
            user=(
                request.user.profile if request.user.is_authenticated else None
            ),
            full_name=full_name,
            email=email,
            phone=phone,
            city="",
            address="",
            delivery_type="",
            payment_type="",
            status="",
        )

        total_cost = 0

        for item in basket_items:
            product = item["product"]
            qty = item["count"]

            OrderItem.objects.create(order=order, product=product, count=qty)
            total_cost += product.price * qty

        order.total_cost = total_cost
        order.save()

        serializer = OrderIdResponseSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailAPIView(APIView):
    def get_object(self, pk: int) -> Optional[Order]:
        if self.request.user.is_authenticated:
            try:
                return Order.objects.get(pk=pk, user=self.request.user.profile)
            except Order.DoesNotExist:
                return None
        return None

    def get(self, request: Request, pk: int) -> Response:
        if not request.user.is_authenticated:
            return Response(
                data={"detail": "Требуется авторизация"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        profile = request.user.profile

        if BASKET_SESSION_KEY in request.session:
            session_basket = request.session.get(BASKET_SESSION_KEY, {})
            if session_basket:
                for pid_str, count in session_basket.items():
                    try:
                        product_id = int(pid_str)
                        basket_item, created = Basket.objects.get_or_create(
                            user=profile,
                            product_id=product_id,
                            defaults={"count": count},
                        )
                        if not created:
                            basket_item.count += count
                            basket_item.save()
                    except ValueError:
                        continue
                del request.session[BASKET_SESSION_KEY]
                request.session.modified = True

        # order = self.get_object(pk)
        # if not order:
        try:
            order = (
                # Order.objects.get(pk=pk, user__isnull=True)
                Order.objects.select_related("user")
                .prefetch_related("items__product")
                .get(pk=pk, user=profile)
            )
        except Order.DoesNotExist:
            order = Order.objects.select_related('user').prefetch_related(
                'items__product'
            ).get(pk=pk, user__isnull=True)

            order.user = profile
            if not order.full_name:
                order.full_name = profile.fullName
            if not order.email:
                order.email = profile.email
            if not order.phone:
                order.phone = profile.phone
            order.save(update_fields=["user", "full_name", "email", "phone"])

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderCreateSerializer(data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        validated = serializer.validated_data
        if "city" in validated:
            order.city = validated["city"]
        if "address" in validated:
            order.address = validated["address"]
        if "deliveryType" in validated:
            order.delivery_type = validated["deliveryType"]
        if "paymentType" in validated:
            order.payment_type = validated["paymentType"]

        if not order.items.exists():
            basket_items = get_basket(request)
            if not basket_items:
                return Response(
                    data={"detail": "Корзина пуста"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            total_cost = 0
            for item in basket_items:
                OrderItem.objects.create(
                    order=order, product=item["product"], count=item["count"]
                )
                total_cost += item["product"].price * item["count"]

            order.total_cost = total_cost

        order.save()

        if request.user.is_authenticated:
            Basket.objects.filter(user=request.user.profile).delete()

        updated_serializer = OrderIdResponseSerializer(order)
        return Response(updated_serializer.data, status=status.HTTP_200_OK)
