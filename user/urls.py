from django.urls import path
from .views import ClientProfileView, AgentProfileView, OwnerProfileView, UserLoginView, UserRegistrationView

urlpatterns = [
    path('profile/client', ClientProfileView.as_view(), name='client-profile'),
    path('profile/agent', AgentProfileView.as_view(), name='agent-profile'),
    path('profile/owner', OwnerProfileView.as_view(), name='owner-profile'), 
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
]