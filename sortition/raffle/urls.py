from django.urls import path
from .views import list_raffles, add_raffles, delete_raffles, detail_raffles, quota_payment, quota_reset


urlpatterns = [
    path("", list_raffles, name="list-raffles"),
    path("add/", add_raffles, name="add-raffles"),
    path("<int:raffle_pk>/delete/", delete_raffles, name="delete-raffles"),
    path("<int:raffle_pk>/detail/", detail_raffles, name="detail-raffles"),
    path("quota/<int:quota_pk>/pay/", quota_payment, name="pay-quota"),
    path("quota/<int:quota_pk>/reset/", quota_reset, name="reset-quota"),
]
