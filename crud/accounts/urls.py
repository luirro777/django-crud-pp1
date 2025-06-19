# urls for accounts app
from django.urls import path
# urls for auth views
from django.contrib.auth import views as auth_views
# views for accounts app
from . import views

app_name = 'accounts'

urlpatterns = [
    path(
        'login/', 
        auth_views.LoginView.as_view(template_name='accounts/login.html'), 
        name='login'
    ),
    path(
        'logout/', 
        auth_views.LogoutView.as_view(), 
        name='logout'
    ),
    path(
        'logout_message',
        views.LogoutMessageView.as_view(),
        name='logout_message'
    ),
    path(
        'signup/', 
        views.SignUpView.as_view(), 
        name='signup'
    ),
]