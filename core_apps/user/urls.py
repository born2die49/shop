from django.urls import path, re_path
from .views import (
    StaffLoginView,
    CustomerLoginView,
    CustomTokenRefreshView,
    LogoutAPIView,
    CustomProviderAuthView,
)

urlpatterns = [
    re_path(
        r"^o/(?P<provider>\S+)/$",
        CustomProviderAuthView.as_view(),
        name="provider-auth",
    ),
    path("customer-login/", CustomerLoginView.as_view(), name="customer_login"),
    path("staff-login/", StaffLoginView.as_view(), name="staff_login"),
    # path("social/", CustomProviderAuthView.as_view(), name="social_login"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
