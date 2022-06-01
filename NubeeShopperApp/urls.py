from unicodedata import name
from NubeeShopperApp import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home"),
    path('signin', views.signin, name="signin"),
    path('signup', views.signup, name="signup"),
    path('signout', views.signout, name="signout"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path("productview/<int:myid>", views.productview, name="productview"),
    path('producttracker', views.producttracker, name="producttracker"),
    path('productsearch', views.productsearch, name="productsearch"),
    path('productpayment', views.productpayment, name="productpayment"),
    path('productcheckout', views.productcheckout, name="productcheckout"),
    path('paymentstatus', views.paymentstatus, name="paymentstatus")
]