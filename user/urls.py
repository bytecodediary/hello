from django.urls import path
from . import views

urlpatterns = [
    path('profile/client/', views.ClientProfileView.as_view(), name='client-profile'),
    path('profile/agent/', views.AgentProfileView.as_view(), name='agent-profile'),
    path('profile/owner/', views.OwnerProfileView.as_view(), name='owner-profile'), 
    path('profile/tenant', views.TenantProfileView.as_view(), name='tenant-profile'),
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("api/v1/auth/register/", views.UserRegistrationView.as_view(), name="api-auth-register"),
    path("api/v1/auth/login/", views.UserLoginView.as_view(), name="api-auth-login"),
    path("api/v1/auth/refresh/", views.CookieTokenRefreshView.as_view(), name="api-auth-refresh"),
    path("api/v1/auth/me/", views.auth_me, name="api-auth-me"),
    path("logout/", views.logout_view, name="logout"),
    path("api/v1/provider/applications/", views.ProviderApplicationCreateView.as_view(), name="api-provider-applications"),
    path("api/v1/provider/applications/<int:pk>/review/", views.ProviderApplicationReviewView.as_view(), name="api-provider-application-review"),
    path("get_csrf_token/", views.get_csrf_token, name="get_csrf_token"),

    path("profile/tenant/", views.TenantProfileView.as_view(), name="tenant-profile"),
    path("appointment/", views.AppointmentView.as_view(), name="appointment"),

    path("check_authentication/", views.check_authentification, name="check_authentification"),

    path("verify/", views.VerificationView.as_view(), name="verify-user"),
]
