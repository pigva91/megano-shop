from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from basket.basket_session import get_basket, add_to_basket, remove_from_basket
from basket.serializers import BasketItemSerializer


class BasketApiView(APIView):
    def get(self, request):
        basket_items = get_basket(request)
        serializer = BasketItemSerializer(basket_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get("id")
        qty = int(request.data.get("count", 1))

        add_to_basket(request, product_id, qty)

        basket_items = get_basket(request)
        serializer = BasketItemSerializer(basket_items, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        product_id = request.data.get("id")
        qty = request.data.get("count")

        remove_from_basket(request, product_id, qty)

        basket_items = get_basket(request)
        serializer = BasketItemSerializer(basket_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
