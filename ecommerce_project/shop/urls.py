from django.urls import path

from shop import views
app_name = 'shop'
urlpatterns = [
    path('allProdCat', views.allProdCat, name='allProdCat'),
    path('', views.front, name='front'),
    path('<slug:c_slug>/',views.allProdCat,name='products_by_category'),
    path('<slug:c_slug>/<slug:product_slug>/', views.prodDetail, name='prodCatDet'),
    path('register', views.register, name='register'),
    path('login_section', views.loginpage, name='login'),
    path('logout', views.logout, name='logout'),
]