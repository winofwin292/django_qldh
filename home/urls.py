from django.urls import path, include
import home.views as views


urlpatterns = [
    path('', views.index, name='home_page'),
]
