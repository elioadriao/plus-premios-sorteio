from django.contrib import admin

from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .raffle import urls as raffles_urls
from .raffle.views import index, list_winners, about
from .account import urls as account_urls


urlpatterns = [
    path("", index, name="index"),
    path("winners/", list_winners, name="list-winners"),
    path("about/", about, name="about"),
    path("account/", include((account_urls, "account"), namespace="account")),
    path("raffles/", include((raffles_urls, "raffle"), namespace="raffles")),
    path("admin/", admin.site.urls),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
