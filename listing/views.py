from .serializers import (
    FavoriteSerializer,
    InquirySerializer,
    InquiryStatusSerializer,
    NotificationMiniSerializer,
    FCMDeviceSerializer,
    PropertySerializer,
)
from rest_framework import status, generics, permissions, serializers
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import Favorite, Inquiry, Property, Notification
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PropertyFilter
from rest_framework.exceptions import PermissionDenied, NotAcceptable
from fcm_django.models import FCMDevice
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.db import IntegrityError, transaction
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from .permissions import CanManageListings, IsApprovedProvider, IsStaff


#property views
class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.select_related("created_by").all().order_by("-listed_at")
    serializer_class = PropertySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = PropertyFilter
    search_fields = ["title", "description", "city", "address"]
    ordering_fields = ["price", "listed_at"]
    ordering = ["-listed_at"]
    permission_classes = [CanManageListings]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method == "GET":
            return queryset.filter(moderation_status="published", status__in=("available", "pending"))
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, moderation_status="pending_review")


class ProviderPropertyListCreateView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsApprovedProvider]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = PropertyFilter
    search_fields = ["title", "description", "city", "address", "county", "neighborhood"]
    ordering_fields = ["price", "listed_at", "updated_at"]
    ordering = ["-updated_at"]

    def get_queryset(self):
        queryset = Property.objects.select_related("created_by").all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, moderation_status="pending_review")


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.select_related("created_by").all()
    serializer_class = PropertySerializer
    permission_classes = [CanManageListings]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and (user.is_staff or user.can_manage_listings):
            return queryset.filter(
                models.Q(moderation_status="published") | models.Q(created_by=user)
            )
        return queryset.filter(moderation_status="published")

    def perform_update(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            serializer.save(moderation_status="pending_review")


class PropertyModerationView(generics.UpdateAPIView):
    queryset = Property.objects.all()
    serializer_class = serializers.Serializer
    permission_classes = [IsStaff]
    lookup_field = "slug"

    def update(self, request, *args, **kwargs):
        property_instance = self.get_object()
        moderation_status = request.data.get("moderation_status")
        valid_statuses = {choice[0] for choice in Property.MODERATION_STATUS_CHOICES}
        if moderation_status not in valid_statuses:
            return Response(
                {"moderation_status": "Choose a valid moderation status."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        property_instance.moderation_status = moderation_status
        property_instance.moderated_by = request.user
        property_instance.moderated_at = timezone.now()
        property_instance.save(update_fields=["moderation_status", "moderated_by", "moderated_at", "updated_at"])
        return Response(PropertySerializer(property_instance, context={"request": request}).data)


class FavoriteToggleView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def post(self, request, slug):
        property_instance = get_object_or_404(Property, slug=slug, moderation_status="published")
        favorite, _ = Favorite.objects.get_or_create(user=request.user, property=property_instance)
        return Response(self.get_serializer(favorite).data, status=status.HTTP_201_CREATED)

    def delete(self, request, slug):
        deleted, _ = Favorite.objects.filter(
            user=request.user,
            property__slug=slug,
        ).delete()
        if not deleted:
            return Response({"detail": "Favorite not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related("property")


class InquiryCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InquirySerializer

    def create(self, request, *args, **kwargs):
        property_instance = get_object_or_404(
            Property,
            slug=kwargs["slug"],
            moderation_status="published",
        )
        if property_instance.created_by_id == request.user.id:
            return Response(
                {"detail": "You cannot inquire about your own listing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            inquiry = serializer.save(property=property_instance, seeker=request.user)
            if property_instance.created_by_id:
                Notification.objects.create(
                    user=property_instance.created_by,
                    message=f"New inquiry received for {property_instance.title}.",
                )
                send_mail(
                    subject=f"New inquiry for {property_instance.title}",
                    message=f"A seeker sent a new {inquiry.inquiry_type} request.",
                    from_email=None,
                    recipient_list=[property_instance.created_by.email],
                    fail_silently=True,
                )
        return Response(self.get_serializer(inquiry).data, status=status.HTTP_201_CREATED)


class SeekerInquiryListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InquirySerializer

    def get_queryset(self):
        return Inquiry.objects.filter(seeker=self.request.user).select_related("property", "seeker")


class ProviderInquiryListView(generics.ListAPIView):
    permission_classes = [IsApprovedProvider]
    serializer_class = InquirySerializer

    def get_queryset(self):
        queryset = Inquiry.objects.select_related("property", "seeker")
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(property__created_by=self.request.user)


class ProviderInquiryUpdateView(generics.UpdateAPIView):
    permission_classes = [IsApprovedProvider]
    serializer_class = InquiryStatusSerializer
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        queryset = Inquiry.objects.all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(property__created_by=self.request.user)

    def perform_update(self, serializer):
        inquiry = serializer.save()
        Notification.objects.create(
            user=inquiry.seeker,
            message=f"The provider replied to your inquiry about {inquiry.property.title}.",
        )
        send_mail(
            subject=f"Update on your inquiry for {inquiry.property.title}",
            message=inquiry.provider_response or f"Your inquiry status is now {inquiry.status}.",
            from_email=None,
            recipient_list=[inquiry.seeker.email],
            fail_silently=True,
        )

# notification views

class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationMiniSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.filter(
            user=user,
            is_read = False
        ).order_by('-received_at')
        return queryset

class NotificationAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationMiniSerializer
    queryset = Notification.objects.all()

    def retrieve(self,request, *args, **kwargs):
        notification = self.get_object()
        if notification.user != request.user:
            raise PermissionDenied(
                'This notification does not belong to you'
            )
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.user != request.user:
            raise PermissionDenied(
                'This notification does not belong to you'
            )
        self.perform_destroy(notification)
        return Response(status=status.HTTP_204_NO_CONTENT)

class MarkAllAsReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = self.request.user
        notifications = Notification.objects.filter(
            user=user, is_read = False
        )

        for notification in notifications:
            if notification.user != request.user:
                raise PermissionDenied(
                    'Action not allowed'
                )
            notification.is_read = True
            notification.save()
        return Response('No new notification', status=status.HTTP_200_OK)

class CreateDeviceAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        user = request.user
        registration_id = request.data.get("registration_id", None)
        type = request.data.get("type", None)
        device = FCMDevice.objects.filter(registration_id=registration_id, type=type)
        if device.count() > 0:
            raise NotAcceptable("This Device already exists.")
        serializer = FCMDeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
