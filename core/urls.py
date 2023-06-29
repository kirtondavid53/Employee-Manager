from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logout_view, name="logout"),
    path("record/<int:pk>", views.record_view, name="record"),
    path("add_employee", views.add_employee, name="add_employee"),
    path('register', views.register, name="register"),
    path("delete_employee/<int:pk>", views.delete_employee, name="delete_employee"),
    path("update_employee/<int:pk>", views.update_employee, name="update_employee"),
    path('search', views.search_records, name='search'),
    path('dashboard', views.dashboard_view, name='dashboard'),
]