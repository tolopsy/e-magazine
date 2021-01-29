from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap 
from blog.sitemaps import PostSitemap



sitemaps = {
    'posts': PostSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('blog-body/', include('ckeditor_uploader.urls')),
    path('', include('blog.urls')),
]


if settings.DEBUG:
	urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


