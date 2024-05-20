from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import redirect, render
from django.urls import include, path, re_path
from django.views.generic import TemplateView, base
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import TokenRefreshView

from axes.decorators import axes_dispatch

from Myapp import views


if settings.DEBUG == True:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()
# router.register('Dossier', views.DossierViewSet,           basename="Dossier" )

class PublicAPISchemeGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.base_path = '/api/' # api/
        return schema

schema_view = get_schema_view(
   openapi.Info(
      title="<Model>_API", swagger= "2.0", openapi = "2.0.0", default_version='V 1.0', description="<Model>_API ENGINE",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="mohammed.chalouli@at.dz"),
      license=openapi.License(name="<Model> License"),
      ),
    generator_class=PublicAPISchemeGenerator, public=True, permission_classes=(permissions.AllowAny,),
)

handler404 = views.Errorhandler404
handler500 = views.Errorhandler500

urlpatterns = [
    # path('__debug__/', include('debug_toolbar.urls')),
    # Userpage ==================================================================================
    path('api/', include(router.urls)),
    path('login/', views.LoginPage,                       name="login"),        
    path('login_post/', views.login_post,                 name="login_post"),        
    path('logout/', views.LogoutPage,                     name="logout"),   
    path('profil/', views.ProfilPage,                     name="profil"),                          
    path('post_profil_page/', views.post_profil_page,     name="profilPost"),                             
    # Admin Panel================================================================================
    path('admin/', include('admin_honeypot.urls',         namespace='admin_honeypot')),
    path('administrator/', admin.site.urls,               name="admin"),                                 
    # JWT =======================================================================================
    path('api/Reset/', views.PasswordReset,           name="resetapi"),  # Reste Password
    # Django - Axes =============================================================================
    path('locked-out/', axes_dispatch(TemplateView.as_view(template_name='lockout.html')), name='axes_locked_out'),
    # Custom =============================================================================
    
    path('', views.IndexPage,   name="index"),       
    path('dashboard/', TemplateView.as_view(template_name='_model.html'), name='dashboard'),
 
    # path('demande/<int:theID>/', views.dossierPage,   name="demande"),       
    
    # On Production ============================================================================
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('favicon.ico', base.RedirectView.as_view(url=('/assets/favicon.png')))
] 
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "<Model> Administration"
admin.site.site_title  = "Panneau d'administration <Model>"
admin.site.index_title = "Bienvenue au portail d'administration du projet <Model>"
