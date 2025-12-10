# frxapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # ... boshqa URL lar ...

    # Login/Register sahifasiga o'tish
    path('', views.login_register_view, name='login_register'),

    # Ro'yxatdan o'tish (Registration) uchun kerak
    path('register/', views.register_user, name='register'),  # <-- BU QATOR KERAK!

    # Tizimga kirish (Login) uchun kerak
    path('login/', views.login_user, name='login'),  # <-- BU QATOR KERAK!

    # Dashboardga o'tish
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # ... (boshqa URL lar) ...
]