from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('b2b-hub/', views.b2b_hub, name='b2b_hub'),
    path('track-order/', views.track_order, name='track_order'),
    path('api/checkout/', views.checkout_view, name='checkout_api'),
    path('order-success/<str:tracking_id>/', views.order_success_view, name='order_success')
]