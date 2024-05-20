import os
import datetime
import mimetypes

from django.conf import settings
from pathlib import Path
from django.http import HttpResponse
from django.contrib.messages import constants as messages
import environ
env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = env('SECRET_KEY')    # Django-environ
DEBUG = False if env('DEBUG') == "False" else True

## ON SERVER========================
# In passenger_wsgi.py : there is only one line 
# from application.wsgi import application
CSRF_FAILURE_VIEW = 'Myapp.views.Errorhandler403'
## SSL==================================
# SECURE_SSL_REDIRECT = False  # True if HTTPS
# SECURE_HSTS_PRELOAD = False  # True if HTTPS
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
## Secure==================================
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
##==================================
ALLOWED_HOSTS = ['127.0.0.1','105.96.104.72']
CORS_ALLOWED_ORIGINS = ['http://127.0.0.1', 'http://105.96.104.72', 'https://105.96.104.72' ]

CSRF_TRUSTED_ORIGINS =  CORS_ALLOWED_ORIGINS
SESSION_EXPIRE_SECONDS = 24 * 60 * 60             # Default unit : Seconds # 2hours
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

SESSION_TIMEOUT_REDIRECT = '/'
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000000

AUTH_USER_MODEL= 'Myapp.UserApp'
AUTH_PROFILE_MODULE  = 'Myapp.AT_User'
# Application definition
INSTALLED_APPS = [
    # My Libraries
    'csp',
    'import_export',
    'Myapp',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'admin_honeypot',
    'debug_toolbar',
    'jazzmin',
    'django_extensions',
    'crispy_forms',
    'crispy_bootstrap5',
    'silk',
    'axes',
    
    # Built-in
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
]
#
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=3),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=30),
    'USER_ID_FIELD': 'username',
    'USER_ID_CLAIM': 'username',
}
JAZZMIN_SETTINGS = {
    "site_brand": "<Model> Admin",
    
    "show_ui_builder": False,
    "welcome_sign": "Welcome to administration panel",
    "copyright": " Unité Recherche & Developpement - Algérie Télécom",
    "custom_css": None,
    "custom_js": None,
    "related_modal_active": True,
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "hide_models": [],
    # "hide_apps": ['admin_honeypot', 'auth' ,'admin'],
    "hide_apps": ['auth' ,'admin'],
    "order_with_respect_to": [ "Myapp.UserApp", "Myapp.Structure","Myapp.AppSettings",],
     "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        # {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        # external url that opens in a new window (Permissions can be added)
        # {"name": "Support", "url": "/URL/", "new_window": True},
        # model admin to link to (Permissions checked against model)
        {"model":   'admin.logentry'},
        {"model":   'auth.group'},
        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "axes"},

    ],

}
JAZZMIN_UI_TWEAKS = {
    # "theme": "journal",  
    "dark_mode_theme": None,
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-blue",
    "sidebar": "sidebar-dark-info",
    "navbar": "navbar-dark  navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    
    "actions_sticky_top": False,
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-success"
    },
}


MIDDLEWARE = [
    'csp.middleware.CSPMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',     # CACHE
    'Myapp.middlewares.RemoveServerHeaderMiddleware',
    'Myapp.middlewares.XContentTypeOptionsMiddleware',     # Override for other types
    'Myapp.middlewares.DisableHttpTraceMiddleware',     
    'Myapp.middlewares.CacheControlMiddleware',     
    'Myapp.middlewares.PermissionsPolicyMiddleware',     
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',  # CACHE
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Should be added --------------------------------------------------------
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'silk.middleware.SilkyMiddleware',
    'axes.middleware.AxesMiddleware', # AxesMiddleware should be the last middleware in the MIDDLEWARE list.
    # 'django.middleware.cache.CacheMiddleware',  
]

# CACHE_MIDDLEWARE_SECONDS = 30  # Cache for 1 minute

IMPORT_EXPORT_IMPORT_PERMISSION_CODE = 'add'
IMPORT_EXPORT_EXPORT_PERMISSION_CODE = 'view'


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

## On Server to hide DRF : 
REST_FRAMEWORK = {  
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/day', # Terminals at each DOT are linked anonymously, I believe that this can rise up to 500
        'user': '1000/day'  # You may turn it to 5 for test purposes, I've implemented an API logger to have the exact amount of the queries needed daily
    }
}
# Silky=========================================================================
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION  = True
SILKY_META           = False
SILKY_MAX_REQUEST_BODY_SIZE = -1  # Silk takes anything <0 as no limit
SILKY_MAX_RESPONSE_BODY_SIZE = 1024  # If response body>1024 bytes, ignore
SILKY_PYTHON_PROFILER = True


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'axes.backends.AxesBackend',
]
AXES_ENABLED = True
AXES_FAILURE_LIMIT = 30

AXES_COOLOFF_TIME = datetime.timedelta(minutes=1)
AXES_VERBOSE = True
AXES_CACHE = 'axes'
LOGIN_URL = '/login/'
AXES_ENABLE_ACCESS_FAILURE_LOG = True
AXES_HTTP_RESPONSE_CODE = 200

AXES_RESET_COOL_OFF_ON_FAILURE_DURING_LOCKOUT = False
AXES_RESET_ON_SUCCESS = True

AXES_LOCK_OUT_AT_FAILURE = True
AXES_LOCKOUT_TEMPLATE = 'lockout.html/'
AXES_LOCKOUT_URL = '/locked-out/'
AXES_LOCKOUT_CALLABLE = 'Myapp.views.user_lockout'

CUSTOM_AXES_SOFT_LOCKOUT_MESSAGE = '300'
CSP_INCLUDE_NONCE_IN = ['script-src','style-src','child-src','object-src','img-src','frame-src','font-src']
CSP_DEFAULT_SRC= ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'"  )
CSP_STYLE_SRC  = ("'self'", "'unsafe-inline'" ,"https://fonts.googleapis.com/" )
CSP_IMG_SRC    = ("'self'", "data:",  )
CSP_FONT_SRC   = ("'self'", "data:", "https://fonts.googleapis.com/")
CSP_CHILD_SRC  = ("'self'", "http://127.0.0.1/" )
CSP_FRAME_SRC  = ("'self'", "http://127.0.0.1/" ,"data:")
X_FRAME_OPTIONS = 'SAMEORIGIN'


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
ROOT_URLCONF = 'application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['template' , os.path.join(BASE_DIR, 'template')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'application.wsgi.application'
# JWT ==============================================================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':  datetime.timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=30),
    'USER_ID_FIELD':  'username',
    'USER_ID_CLAIM':  'username',
    'ROTATE_REFRESH_TOKENS': False,
}
SWAGGER_SETTINGS = {
    #'USE_SESSION_AUTH': False,
    
    'USE_SESSION_AUTH': True,       # add Django Login and Django Logout buttons, CSRF token to swagger UI page
    'LOGIN_URL': '/administrator/',  # URL for the login button
    'LOGOUT_URL': '/logout/',        # URL for the logout button

    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },  

    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     env('DB_NAME'),     
        'USER':     env('DB_USER'),     
        'PASSWORD': env('DB_PASSWORD'), 
        'HOST':     env('DB_HOST'),     
        'PORT':     env('DB_PORT'),     
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {   'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {   'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': { 'min_length': 8, } },
    {   'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {   'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Africa/Algiers'
USE_I18N = True
USE_L10N = True
USE_TZ = False
USE_THOUSAND_SEPARATOR = False
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000000


mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/javascript", ".js", True)

APPEND_SLASH = True
STATICFILES_DIRS = [BASE_DIR / 'assets/']

STATIC_ROOT = BASE_DIR / 'template' / 'assets'
MEDIA_ROOT = BASE_DIR / 'template' / 'media'

STATIC_URL = '/assets/'
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_USE_TLS       = env('EMAIL_USE_TLS'),
EMAIL_HOST          = env('EMAIL_HOST'),
EMAIL_PORT          = env('EMAIL_PORT'),
DEFAULT_FROM_EMAIL  = env('DEFAULT_FROM_EMAIL'),
EMAIL_HOST_USER     = env('EMAIL_HOST_USER'),
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD'),

DEFAULT_PASSWORD = env('DEFAULT_PASSWORD'),

MESSAGE_TAGS = {     messages.ERROR: 'danger', }
VALID_EXTENSION = ['pdf', 'docx', 'doc', 'jpg', 'jpeg', 'png', 'xlsx', 'xls']
VALID_CONTENT   = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                            'image/jpeg', 'image/png', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                            'application/msword', 'application/vnd.ms-excel']