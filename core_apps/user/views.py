import logging

from django.contrib.auth import get_user_model
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.permissions import AllowAny
from djoser.signals import user_registered

from core_apps.common.utils import set_auth_cookies
from core_apps.user.serializers import CreateCustomerSerializer

User = get_user_model()
logger = logging.getLogger(__name__)


class StaffLoginView(TokenObtainPairView):
    """
    Dedicated Login View for Staff/Admins.
    - Security: High
    - Checks: is_staff=True
    - Session Duration: Short (e.g., 1 hour access, 12 hours refresh)
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            # 1. Generate Token
            token_res = super().post(request, *args, **kwargs)

            if token_res.status_code == status.HTTP_200_OK:
                user_email = request.data.get("email")

                # 2. Check User Role (STRICT CHECK)
                try:
                    user = User.objects.get(email=user_email)

                    if not user.is_staff:
                        logger.warning(
                            f"Unauthorized staff login attempt by: {user_email}"
                        )
                        return Response(
                            {
                                "detail": "Access Denied. You do not have staff permissions."
                            },
                            status=status.HTTP_403_FORBIDDEN,
                        )
                except User.DoesNotExist:
                    return Response(
                        {"detail": "User not found"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

            # 3. Set Short Lifetimes for Security
            # Staff Access: 1 Hour (3600 sec), Refresh: 12 Hours
            access_token = token_res.data.get("access")
            refresh_token = token_res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(
                    token_res,
                    access_token=access_token,
                    refresh_token=refresh_token,
                    access_max_age=3600,  # 1 Hour
                    refresh_max_age=3600 * 12,  # 12 Hours
                )

                # 4. Cleanup Response
                token_res.data.pop("access", None)
                token_res.data.pop("refresh", None)
                token_res.data["message"] = "Staff Login Successful"
                token_res.data["role"] = "staff"

            return token_res

        except (InvalidToken, TokenError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class CustomerLoginView(TokenObtainPairView):
    """
    Login View for Regular Customers.
    - Security: Standard
    - Session Duration: Long (e.g., 24 hours access, 7 days refresh)
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            token_res = super().post(request, *args, **kwargs)

            if token_res.status_code == status.HTTP_200_OK:
                # 1. No strict role check needed, but verify active
                # Optional: Can block staff from logging in here

                access_token = token_res.data.get("access")
                refresh_token = token_res.data.get("refresh")

                if access_token and refresh_token:
                    # 2. Set Long Lifetimes for Better UX
                    # Customer Access: 1 Day, Refresh: 7 Days
                    set_auth_cookies(
                        token_res,
                        access_token=access_token,
                        refresh_token=refresh_token,
                        access_max_age=86400,  # 1 Day
                        refresh_max_age=86400 * 7,  # 7 Days
                    )

                    # 3. Cleanup Response
                    token_res.data.pop("access", None)
                    token_res.data.pop("refresh", None)
                    token_res.data["message"] = "Login Successful"
                    token_res.data["role"] = "customer"

                return token_res

        except (InvalidToken, TokenError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class CustomTokenRefreshView(TokenRefreshView):
    # Custom view for refreshing access tokens.
    def post(self, request: Request, *args, **kwargs) -> Response:
        # Extract the refresh token from the incoming cookie.
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            # Manually add the refresh token to the request data for the parent view to process.
            request.data["refresh"] = refresh_token

        refresh_res = super().post(request, *args, **kwargs)

        if refresh_res.status_code == status.HTTP_200_OK:
            access_token = refresh_res.data.get("access")
            new_refresh_token = refresh_res.data.get(
                "refresh"
            )  # a new refresh token if ROTATE_REFRESH_TOKENS is True

            if access_token and refresh_token:
                try:
                    token = AccessToken(access_token)
                    user_id = token["user_id"]
                    user = User.objects.get(id=user_id)

                    # set lifetime based on role
                    if user.is_staff:
                        access_max_age = 3600  # 1 Hour
                        refresh_max_age = 3600 * 12  # 12 Hours
                    else:
                        access_max_age = 86400  # 1 Day
                        refresh_max_age = 86400 * 7  # 7 Days

                    set_auth_cookies(
                        refresh_res,
                        access_token=access_token,
                        refresh_token=new_refresh_token,
                        access_max_age=access_max_age,
                        refresh_max_age=refresh_max_age,
                    )

                except Exception as e:
                    logger.error(f"Error setting cookies in refresh view: {str(e)}")

                refresh_res.data.pop("access", None)
                refresh_res.data.pop("refresh", None)

                refresh_res.data["message"] = "Access token refreshed successfully"
            else:
                refresh_res.data["message"] = (
                    "Access or Refresh token not found in refresh response data"
                )
                logger.error(
                    "Access or Refresh token not found in refresh response data"
                )

        return refresh_res


class CustomProviderAuthView(ProviderAuthView):
    # Custom view for social authentication (e.g., Google).
    def post(self, request: Request, *args, **kwargs) -> Response:
        # Let Djoser's view handle the social authentication process.
        provider_res = super().post(request, *args, **kwargs)

        if provider_res.status_code == status.HTTP_201_CREATED:
            access_token = provider_res.data.get("access")
            refresh_token = provider_res.data.get("refresh")

            if access_token and refresh_token:
                # After successful social login, set the authentication cookies.
                set_auth_cookies(
                    provider_res,
                    access_token=access_token,
                    refresh_token=refresh_token,
                    access_max_age=86400,  # 1 Day (Customer Time)
                    refresh_max_age=86400 * 7,  # 7 Days (Customer Time)
                )

                provider_res.data.pop("access", None)
                provider_res.data.pop("refresh", None)

                provider_res.data["message"] = "You are logged in Successfully"
            else:
                provider_res.data["message"] = (
                    "Access or Refresh token not found in provider response"
                )
                logger.error(
                    "Access or Refresh token not found in provider response data"
                )

        return provider_res


class LogoutAPIView(APIView):
    # API view for user logout.
    def post(self, request: Request, *args, **kwargs):
        # Create a response that doesn't need a body, as is standard for logout.
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        response.delete_cookie("logged_in")
        return response
