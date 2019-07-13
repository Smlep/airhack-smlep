from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('entry', views.entry, name='entry'),
    path('request/<int:id>', views.request_details, name='request_details')
]