from django.urls import path

from cart import views

app_name = 'cart'
urlpatterns = [
    path('add/<int:product_id>/', views.addcart, name='add_cart'),
    path('', views.CartDetails, name='CartDetails'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('delete/<int:product_id>/', views.car_delete_all, name='cart_delete')
]
