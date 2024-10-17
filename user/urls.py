from django.urls import path
from . import views

urlpatterns = [
    path('profile/client', views.ClientProfileView.as_view(), name='client-profile'),
    path('profile/agent', views.AgentProfileView.as_view(), name='agent-profile'),
    path('profile/owner', views.OwnerProfileView.as_view(), name='owner-profile'), 
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
]