from pathlib import Path
from dotenv import load_dotenv
import os

# ==================================================
# BASE Y ENV
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# ==================================================
# CLAVES Y DEBUG
# ==================================================

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "tiendagenesis.onrender.com",
]

# ==================================================
# CLOUDINARY
# ==================================================

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}



# ==================================================
# GOOGLE LOGIN
# ==================================================

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "").strip()

GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "").strip()

GOOGLE_LOGIN_ENABLED = bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET)

# ==================================================
# APPS
# ==================================================

INSTALLED_APPS = [

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps proyecto
    'TiendaGenesisApp',
    'informacion',
    'contacto',
    'tienda',
    'carrito',

    # Cloudinary
    'cloudinary',
    'cloudinary_storage',

    # Allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1

# ==================================================
# AUTH
# ==================================================

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# ==================================================
# MIDDLEWARE
# ==================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'allauth.account.middleware.AccountMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==================================================
# URLS
# ==================================================

ROOT_URLCONF = 'TiendaGenesis.urls'

# ==================================================
# TEMPLATES
# ==================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [BASE_DIR / "templates"],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

                'TiendaGenesis.context_processors.auth_settings',
            ],
        },
    },
]

# ==================================================
# WSGI
# ==================================================

WSGI_APPLICATION = 'TiendaGenesis.wsgi.application'

# ==================================================
# DATABASE
# ==================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==================================================
# INTERNACIONALIZACIÓN
# ==================================================

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True

# ==================================================
# STATIC
# ==================================================

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==================================================
# MEDIA
# ==================================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },

    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# ==================================================
# EMAIL
# ==================================================

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "").strip()

GMAIL_EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "").strip()

GMAIL_EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "").strip()

EMAIL_DELIVERY_ENABLED = bool(
    SENDGRID_API_KEY or (GMAIL_EMAIL_HOST_USER and GMAIL_EMAIL_HOST_PASSWORD)
)

if SENDGRID_API_KEY:
    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
elif GMAIL_EMAIL_HOST_USER and GMAIL_EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = GMAIL_EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = GMAIL_EMAIL_HOST_PASSWORD
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    GMAIL_EMAIL_HOST_USER or "camilo.rubiano@estudiantesunibague.edu.co"
)

CONTACT_EMAIL = os.getenv(
    "CONTACT_EMAIL",
    "camilo.rubiano@estudiantesunibague.edu.co"
)

SENDGRID_SANDBOX_MODE_IN_DEBUG = False

SENDGRID_TRACK_EMAILS = False

# ==================================================
# LOGIN
# ==================================================

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

ACCOUNT_LOGIN_METHODS = {'email'}

ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_QUERY_EMAIL = True

SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": GOOGLE_CLIENT_ID,
            "secret": GOOGLE_CLIENT_SECRET,
            "key": ""
        },
        "AUTH_PARAMS": {
            "prompt": "select_account"
        },
        "LOCALE_FUNC": lambda request: "es",
    }
}

# ==================================================
# DEFAULT FIELD
# ==================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
