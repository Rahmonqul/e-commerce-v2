"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

swagger_info = openapi.Info(
    title="API Documentation",
    default_version='v1',
    description="Документация API вашего проекта",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="support@example.com"),
    license=openapi.License(name="BSD License"),
)

swagger_info = openapi.Info(
    title="API with Bearer Token",
    default_version='v1',
    description="API с поддержкой Bearer токенов (JWT)",
)

swagger_schema_view = get_schema_view(
    swagger_info,
    public=True,
    permission_classes=(AllowAny,),
    authentication_classes=[JWTAuthentication],
)
urlpatterns = [

]


urlpatterns += i18n_patterns(


    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),
    path('api/vendor/', include('vendor.urls')),
    path('api/auth/', include('usauth.urls')),
    path('api/customer/', include('customer.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('swagger/', swagger_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)