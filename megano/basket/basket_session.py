from basket.models import Basket
from catalog.models import Product


BASKET_SESSION_KEY = "basket"


def get_basket(request):
    """
    Возвращает содержимое корзины в формате:
    список словарей с ключами "product" и "count".
    """
    if request.user.is_authenticated:
        queryset = Basket.objects.filter(
            user=request.user.profile
        ).select_related("product")
        return [
            {"product": item.product, "count": item.count} for item in queryset
        ]
    basket = request.session.get(BASKET_SESSION_KEY, {})
    if not basket:
        return []

    products = Product.objects.filter(id__in=basket.keys()).select_related(
        "category"
    )
    prod_dict = {str(p.id): p for p in products}

    return [
        {"product": prod_dict[pid], "count": cnt}
        for pid, cnt in basket.items()
        if pid in prod_dict
    ]


def add_to_basket(request, product_id: int, qty: int = 1):
    if request.user.is_authenticated:
        basket_item, created = Basket.objects.get_or_create(
            user=request.user.profile,
            product_id=product_id,
            defaults={"count": qty},
        )
        if not created:
            basket_item.count += qty
            basket_item.save()
    else:
        basket = request.session.get(BASKET_SESSION_KEY, {})
        pid = str(product_id)
        basket[pid] = basket.get(pid, 0) + qty
        request.session[BASKET_SESSION_KEY] = basket
        request.session.modified = True


def remove_from_basket(request, product_id: int, qty: int = None):
    if request.user.is_authenticated:
        item = Basket.objects.get(
            user=request.user.profile, product_id=product_id
        )
        if qty is None or item.count <= qty:
            item.delete()
        else:
            item.count -= qty
            item.save()
    else:
        basket = request.session.get(BASKET_SESSION_KEY, {})
        pid = str(product_id)
        if pid in basket:
            if qty is None or basket[pid] <= qty:
                del basket[pid]
            else:
                basket[pid] -= qty
            request.session[BASKET_SESSION_KEY] = basket
            request.session.modified = True
