from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from .models import Client, Agent, Owner, CustomUser, ProviderApplication, Tenant, Verification, Appointment
from .serializers import AgentSerializer, ClientSerializer, OwnerSerializer, ChangeUserTypeSerializer, CustomUserSerializer, LoginSerializer, ProviderApplicationSerializer, TenantSerializer, AppointmentSerializer, VerificationSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from .serializers import AgentSerializer, ClientSerializer, OwnerSerializer, ChangeUserTypeSerializer, CustomUserSerializer, LoginSerializer, VerificationSerializer, TenantSerializer  # noqa: F811
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import logout
from .authentication import enforce_csrf

#custom user views
class ChangeUserTypeView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ChangeUserTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProviderApplicationCreateView(generics.ListCreateAPIView):
    serializer_class = ProviderApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return ProviderApplication.objects.select_related('user', 'reviewed_by').all()
        return ProviderApplication.objects.filter(user=self.request.user).select_related('user')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProviderApplicationReviewView(generics.UpdateAPIView):
    queryset = ProviderApplication.objects.select_related('user')
    serializer_class = ProviderApplicationSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        application = self.get_object()
        next_status = request.data.get('status')
        if next_status not in {'approved', 'rejected'}:
            return Response({'status': 'Choose approved or rejected.'}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            application.status = next_status
            application.review_notes = request.data.get('review_notes', '')
            application.reviewed_by = request.user
            application.reviewed_at = timezone.now()
            application.save(update_fields=['status', 'review_notes', 'reviewed_by', 'reviewed_at', 'updated_at'])
            user = application.user
            user.provider_status = next_status
            user.is_pending_type_change = False
            if next_status == 'approved':
                user.user_type = application.requested_type
            user.save(update_fields=['provider_status', 'is_pending_type_change', 'user_type'])
        return Response(ProviderApplicationSerializer(application).data)
    
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return validation errors instead of data on failure
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            response = Response({
                'message': 'login successful',
                'user': {
                    'id': str(user.id),
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'user_type': user.user_type,
                    'provider_status': user.provider_status,
                }
            }, status=status.HTTP_200_OK)
            set_auth_cookies(response, str(refresh.access_token), str(refresh))
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#profiles
class AgentProfileView(generics.RetrieveAPIView):
    queryset = Agent.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AgentSerializer

    def get_object(self):
        try:
            return Agent.objects.select_related("agent").get(agent=self.request.user)
        except Agent.DoesNotExist as exc:
            raise NotFound("Agent profile not found") from exc


class ClientProfileView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClientSerializer

    def get_object(self):
        try:
            return Client.objects.select_related("customer").get(customer=self.request.user)
        except Client.DoesNotExist as exc:
            raise NotFound("Client profile not found") from exc
    

class OwnerProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    def get_object(self):
        try:
            return Owner.objects.select_related("owner", "properties").get(owner=self.request.user)
        except Owner.DoesNotExist as exc:
            raise NotFound("Owner profile not found") from exc


class TenantProfileView(generics.RetrieveAPIView):
    queryset = Tenant.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TenantSerializer

    def get_object(self):
        tenant, _ = Tenant.objects.select_related("name", "rent_status").get_or_create(
            name=self.request.user,
            defaults={
                "email": self.request.user.email,
            },
        )
        return tenant


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})

class AppointmentView(generics.GenericAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_objects(self):
        return self.request.user.username

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def check_authentification(request):
    user = request.user if request.user and request.user.is_authenticated else None
    if user:
        return Response({
            "authenticated": True,
            "username": user.username,
            "email": user.email,
        })
    return Response({"authenticated": False})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def logout_view(request):
    enforce_csrf(request)
    raw_refresh = request.COOKIES.get(settings.AUTH_REFRESH_COOKIE)
    if raw_refresh:
        try:
            RefreshToken(raw_refresh).blacklist()
        except TokenError:
            pass
    logout(request)
    response = Response({"message": "Logged out"}, status=status.HTTP_200_OK)
    response.delete_cookie("sessionid")
    response.delete_cookie("csrftoken")
    response.delete_cookie(settings.AUTH_ACCESS_COOKIE)
    response.delete_cookie(settings.AUTH_REFRESH_COOKIE)
    return response


def set_auth_cookies(response, access_token, refresh_token):
    cookie_options = {
        "httponly": True,
        "secure": settings.AUTH_COOKIE_SECURE,
        "samesite": settings.AUTH_COOKIE_SAMESITE,
    }
    response.set_cookie(
        settings.AUTH_ACCESS_COOKIE,
        access_token,
        max_age=int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()),
        **cookie_options,
    )
    response.set_cookie(
        settings.AUTH_REFRESH_COOKIE,
        refresh_token,
        max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        **cookie_options,
    )


class CookieTokenRefreshView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        enforce_csrf(request)
        raw_refresh = request.COOKIES.get(settings.AUTH_REFRESH_COOKIE)
        if not raw_refresh:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            serializer = TokenRefreshSerializer(data={"refresh": raw_refresh})
            serializer.is_valid(raise_exception=True)
            tokens = serializer.validated_data
            response = Response({"message": "Token refreshed."}, status=status.HTTP_200_OK)
            set_auth_cookies(response, tokens["access"], tokens.get("refresh", raw_refresh))
            return response
        except TokenError as exc:
            raise InvalidToken(str(exc)) from exc


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def auth_me(request):
    user = request.user
    return Response({
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_type": user.user_type,
        "provider_status": user.provider_status,
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def deprecated_token_endpoint(request):
    return Response(
        {"detail": "Bearer token endpoints are retired. Use the HttpOnly cookie authentication endpoints."},
        status=status.HTTP_410_GONE,
    )
  
class VerificationView(generics.GenericAPIView):
    serializer_class = VerificationSerializer
    queryset = Verification.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.data.get('token', None)
        if not token:
            return Response({'error': 'Verification token is required'}, status=status.HTTP_400_BAD_REQUEST)
        verification = Verification.objects.filter(user=request.user, token=token).first()
        if verification is None:
            return Response({'error': 'Verification token not found'}, status=status.HTTP_404_NOT_FOUND)
        if verification.is_verified:
            return Response({'error': 'User is already verified'}, status=status.HTTP_400_BAD_REQUEST)
        if verification.is_token_expired():
            verification.status = 'rejected'
            verification.save(update_fields=['status'])
            return Response({'error': 'Verification token expired'}, status=status.HTTP_400_BAD_REQUEST)
        verification.is_verified = True
        verification.status = 'verified'
        verification.save(update_fields=['is_verified', 'status'])
        return Response({'message': 'User verification successful', 'status': verification.status}, status=status.HTTP_200_OK)
