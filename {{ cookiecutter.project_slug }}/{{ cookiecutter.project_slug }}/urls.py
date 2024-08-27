from django.views.generic import TemplateView
from coderedcms import (
    admin_urls as crx_admin_urls,
    search_urls as crx_search_urls,
    urls as crx_urls
)
from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from wagtail.documents import urls as wagtaildocs_urls


urlpatterns = [
    # Admin
    path("django-admin/", admin.site.urls),
    path("admin/", include(crx_admin_urls)),
    # Documents
    path("docs/", include(wagtaildocs_urls)),
    # Search
    path("search/", include(crx_search_urls)),
    # For anything not caught by a more specific rule above, hand over to
    # the page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(crx_urls)),
]


# fmt: off
if settings.DEBUG:
    from django.conf.urls.static import static

    # Serve static and media files from development server
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore
    urlpatterns += [path("404/", TemplateView.as_view(template_name="404.html"))]

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns
# fmt: on
