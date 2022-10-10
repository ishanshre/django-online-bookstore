from django.urls import path
from . import views


app_name = 'follow'
urlpatterns = [
    path('add_follow/<slug:slug>/', views.AddFollow.as_view(), name='add_follow'),
    path('remove_follow/<slug:slug>/', views.RemoveFollow.as_view(), name='remove_follow'),
]