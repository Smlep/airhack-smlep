from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('entry', views.entry, name='entry'),
    path('request/<int:id>', views.request_details, name='request_details'),
    path('custom_offline', views.custom_offline, name='custom_offline'),
    path('custom_offline_request', views.custom_offline_request, name='custom_offline_request'),
    path('last_cached', views.last_cached_request, name='last_cached')
]