from django.contrib import admin

from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .raffle import urls as raffles_urls
from .account import urls as account_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", raffles_urls.list_raffles, name="index"),
    path("account/", include((account_urls, "account"), namespace="account")),
    path("raffles/", include((raffles_urls, "raffle"), namespace="raffles")),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
