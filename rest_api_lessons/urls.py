from product import views

from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="radomir_test",
        default_version='v1',
        description="month5",
        terms_of_service="https://www.geeks36_1.com/terms/",
        contact=openapi.Contact(email="kingradomir@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/test/', views.test),
    path('', views.product_list_view),
    path('api/v1/product_list/<int:id>/', views.product_detail_view),
    path('api/v1/login/', views.authorization),
    path('api/v1/register/', views.registration),
    path('api/v1/user/reviews/', views.user_reviews),
    path('api/v1/cbv/', include('main_app.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
