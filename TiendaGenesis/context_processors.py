from django.conf import settings


def auth_settings(request):
    return {
        "GOOGLE_LOGIN_ENABLED": settings.GOOGLE_LOGIN_ENABLED,
        "EMAIL_DELIVERY_ENABLED": settings.EMAIL_DELIVERY_ENABLED,
        "CONTACT_EMAIL": settings.CONTACT_EMAIL,
    }
