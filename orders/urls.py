from django.urls import path
from .views import CreateOrderView, MyOrdersView, OrderDetailView, AllOrdersView, UpdateOrderStatusView

urlpatterns = [
    path('',                 CreateOrderView.as_view()),
    path('my/',              MyOrdersView.as_view()),
    path('<int:pk>/',        OrderDetailView.as_view()),
    path('all/',             AllOrdersView.as_view()),
    path('<int:pk>/status/', UpdateOrderStatusView.as_view()),
]
