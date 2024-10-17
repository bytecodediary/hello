from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
namespace = 'main'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("listing.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('order', include('order.urls')),
    path('payment', include('payment.urls')),
    path('user', include('user.urls')),
    path('user/', include('user.urls'))
]
