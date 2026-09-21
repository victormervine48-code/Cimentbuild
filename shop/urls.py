from django.contrib import admin
from django.urls import path
from shop.store import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", views.health, name="health"),
    path("", views.home, name="home"),
    path("produit/<int:pk>/", views.product_detail, name="product_detail"),
    path("panier/", views.cart, name="cart"),
    path("panier/ajouter/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("panier/modifier/<int:pk>/", views.update_cart, name="update_cart"),
    path("panier/supprimer/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
    path("commande/", views.checkout, name="checkout"),
    path("commande/<int:pk>/", views.order_detail, name="order_detail"),
    path("tableau-de-bord/", views.dashboard, name="dashboard"),
]
