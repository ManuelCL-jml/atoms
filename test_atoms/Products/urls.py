from django.urls import path

from rest_framework import routers

from Products.views import RegisterProduct, ListProducts

routers = routers.SimpleRouter()

routers.register(r'RegisterProduct/create', RegisterProduct, basename='register-product')

urlpatterns = [
      path('FilterSize/list',ListProducts.as_view()),
] + routers.urls
