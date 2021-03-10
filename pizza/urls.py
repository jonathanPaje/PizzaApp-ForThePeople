from django.urls import path   
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('createPizza', views.createPizzaPage),
    path('makepizza', views.makepizza),
    path('addcart/<int:pizza_id>', views.addcart),
    path('account', views.account),
    path('order', views.order),
    path('surpriseMe', views.surpriseMe),
    path('complete', views.paymentComplete, name='complete'),
    path('update', views.update),
    path('favorite/<int:pizza_id>',views.favorite),
    path('favoritePage', views.favoritepage),
]