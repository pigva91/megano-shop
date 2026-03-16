from django.urls import path

from .views import (
    BannersAPIView,
    CatalogListAPIView,
    CategoriesAPIView,
    ProductDetailsAPIView,
    ProductsLimitedAPIView,
    ProductsPopularAPIView,
    TagsAPIView,
    ReviewCreateAPIView,
    SalesListAPIView,
)


app_name = "catalog"

urlpatterns = [
    path("categories/", CategoriesAPIView.as_view(), name="categories"),
    path("catalog/", CatalogListAPIView.as_view(), name="catalog"),
    path(
        "catalog/<int:id>/",
        CatalogListAPIView.as_view(),
        name="catalog-by-category",
    ),
    path(
        "products/popular/",
        ProductsPopularAPIView.as_view(),
        name="products-popular",
    ),
    path(
        "products/limited/",
        ProductsLimitedAPIView.as_view(),
        name="products-limited",
    ),
    path(
        "product/<int:id>/",
        ProductDetailsAPIView.as_view(),
        name="product-details",
    ),
    path(
        "product/<int:id>/reviews",
        ReviewCreateAPIView.as_view(),
        name="review-create",
    ),
    path("tags/", TagsAPIView.as_view(), name="tags"),
    path("tags/<int:id>/", TagsAPIView.as_view(), name="tags-detail"),
    path("sales/", SalesListAPIView.as_view(), name="sales"),
    path("banners/", BannersAPIView.as_view(), name="banners"),
]
