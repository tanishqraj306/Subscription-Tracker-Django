from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('list/', views.subscription_list, name='subscription_list'),
    path('monthly/', views.monthly_subscriptions, name='monthly_subscriptions'),
    path('yearly/', views.yearly_subscriptions, name='yearly_subscriptions'),
    path('add/', views.add_subscription, name='add_subscription'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/edit/<int:category_id>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:category_id>/', views.category_delete, name='category_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('mark_as_paid/<int:subscription_id>/', views.mark_as_paid, name='mark_as_paid'),
]