from django.urls import path

from . import views

urlpatterns = [
    path("", views.customer_list, name="customer_list"),
    path("customers/<int:customer_id>/delete/", views.customer_delete, name="customer_delete"),
    path("api/customers/", views.customer_api, name="customer_api"),
]
