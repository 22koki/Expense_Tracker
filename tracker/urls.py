from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("transactions/", views.transaction_list, name="transactions"),
    path("transactions/add/", views.transaction_create, name="transaction_create"),
    path("transactions/<int:pk>/edit/", views.transaction_update, name="transaction_update"),
    path("transactions/<int:pk>/delete/", views.transaction_delete, name="transaction_delete"),
    path("categories/", views.categories, name="categories"),
    path("reports/export/", views.export_csv, name="export_csv"),
    path("accounts/register/", views.register, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
]
