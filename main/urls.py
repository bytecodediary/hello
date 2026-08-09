from django.contrib import admin
from django.urls import path, include
from user.views import deprecated_token_endpoint

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("listing.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path('api/token/', deprecated_token_endpoint, name='deprecated_token_obtain_pair'),
    path('api/token/refresh/', deprecated_token_endpoint, name='deprecated_token_refresh'),
    path('order/', include('order.urls')),
    path('payment/', include('payment.urls')),
    path('user/', include('user.urls')),
    # path('frontend/', include("frontend.urls")),
]
