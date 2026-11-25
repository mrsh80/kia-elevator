from django.urls import path

from . import views


app_name = "dashboard"


urlpatterns = [

    # Dashboard
    path("", views.dashboard_home, name="home"),

    # Products
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_update, name="product_update"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),

    # Categories
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.category_create, name="category_create"),
    path("categories/<int:pk>/edit/", views.category_update, name="category_update"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),

    # Contact Messages
    path("messages/", views.message_list, name="message_list"),
    path("messages/<int:pk>/", views.message_detail, name="message_detail"),
    path("messages/<int:pk>/delete/", views.message_delete, name="message_delete"),
    path("messages/<int:pk>/unread/", views.message_mark_unread, name="message_mark_unread"),
]