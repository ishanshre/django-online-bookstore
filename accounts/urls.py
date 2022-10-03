from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
app_name = 'accounts'
urlpatterns = [
    path('signup/', views.UserSignUpView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/change', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('password/reset', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('resend_activate/', views.ResendActivateAccounts.as_view(), name='resend_activate')
]