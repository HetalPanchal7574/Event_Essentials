from django.urls import path
from . import views
from .views import payment
# from Crypto.Cipher import AES


urlpatterns = [
   
    path("",views.index,name="ShopHome"),
    path("about/",views.about,name="AboutUs"),
    path("contact/",views.contact,name="ContactUs"),
    path("tracker/",views.tracker,name="Tracker"),
    path("search/",views.search,name="Search"),
    path("checkout/",views.checkout,name="Checkout"),
    path('rent/', views.rent, name='rent'),
    path('theme/', views.theme, name='theme'),
    path('logout', views.logout_view, name='logout'),
    path('login', views.LoginPage, name='LoginPage'),
    path('privacypolicy/', views.privacypolicy, name='privacypolicy'),
    path('payment/',payment, name='payment'),
    
]
