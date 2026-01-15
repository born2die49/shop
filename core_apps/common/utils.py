from typing import Optional
from django.conf import settings
from rest_framework.response import Response

def set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: Optional[str] = None,
    access_max_age: Optional[int] = None,
    refresh_max_age: Optional[int] = None,
) -> None:
    """
    Sets HttpOnly cookies for access and refresh tokens.
    Allows overriding max_age for different user roles (Staff vs Customer).
    """
    # 1. Default lifetimes from settings if not provided
    if access_max_age is None:
        access_max_age = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
        
    if refresh_max_age is None:
        refresh_max_age = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
        
    # 2. Base Cookie Settings
    cookie_settings = {
        "path": settings.COOKIE_PATH,
        "secure": settings.COOKIE_SECURE,     # True in Production (HTTPS)
        "httponly": settings.COOKIE_HTTPONLY, # True (Prevent XSS)
        "samesite": settings.COOKIE_SAMESITE, # 'Lax' or 'None'
    }
    
    # 3. Set Access Token Cookie
    response.set_cookie(
        key=settings.COOKIE_NAME, # e.g., "access"
        value=access_token,
        max_age=access_max_age,
        **cookie_settings
    )

    # 4. Set Refresh Token Cookie
    if refresh_token:
        refresh_cookie_settings = cookie_settings.copy()
        response.set_cookie(
            key="refresh",
            value=refresh_token,
            max_age=refresh_max_age,
            **refresh_cookie_settings
        )

    # 5. Set 'logged_in' flag (Not HttpOnly - readable by frontend JS)
    logged_in_cookie_settings = cookie_settings.copy()
    logged_in_cookie_settings["httponly"] = False
    response.set_cookie(
        key="logged_in",
        value="true",
        max_age=access_max_age, # Sync with access token
        **logged_in_cookie_settings
    )