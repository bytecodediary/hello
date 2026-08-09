from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import CustomUser, ProviderApplication


class AuthenticationApiTest(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.user = CustomUser.objects.create_user(
            username="auth-user",
            email="auth@example.com",
            password="password123",
            first_name="Auth",
        )

    def test_login_sets_http_only_auth_cookies(self):
        response = self.client.post(
            "/user/api/v1/auth/login/",
            {"email": "auth@example.com", "password": "password123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("token", response.data)
        self.assertIn("realestate_access", response.cookies)
        self.assertTrue(response.cookies["realestate_access"]["httponly"])
        self.assertIn("realestate_refresh", response.cookies)

    def test_cookie_authentication_can_fetch_current_user(self):
        login_response = self.client.post(
            "/user/api/v1/auth/login/",
            {"email": "auth@example.com", "password": "password123"},
            format="json",
        )

        response = self.client.get("/user/api/v1/auth/me/")

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "auth@example.com")

    def test_cookie_authentication_requires_csrf_for_state_changes(self):
        self.client.post(
            "/user/api/v1/auth/login/",
            {"email": "auth@example.com", "password": "password123"},
            format="json",
        )

        response = self.client.post(
            "/user/api/v1/provider/applications/",
            {"requested_type": "landlord"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logout_clears_cookie_authentication(self):
        self.client.post(
            "/user/api/v1/auth/login/",
            {"email": "auth@example.com", "password": "password123"},
            format="json",
        )
        self.client.get("/user/get_csrf_token/")
        csrf_token = self.client.cookies["csrftoken"].value

        response = self.client.post(
            "/user/logout/",
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get("/user/api/v1/auth/me/").status_code, status.HTTP_401_UNAUTHORIZED)


class ProviderApplicationApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="applicant",
            email="applicant@example.com",
            password="password123",
        )
        self.admin = CustomUser.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password123",
        )

    def test_user_can_apply_to_become_a_provider(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            "/user/api/v1/provider/applications/",
            {"requested_type": "landlord", "organization_name": "Applicant Homes"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ProviderApplication.objects.filter(user=self.user, status="pending").exists())

    def test_admin_approval_promotes_provider(self):
        application = ProviderApplication.objects.create(user=self.user, requested_type="agent")
        self.client.force_authenticate(self.admin)

        response = self.client.patch(
            f"/user/api/v1/provider/applications/{application.pk}/review/",
            {"status": "approved", "review_notes": "Verified"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.user_type, "agent")
        self.assertEqual(self.user.provider_status, "approved")
