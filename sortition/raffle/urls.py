from django.urls import path
from .views import list_raffles, add_raffles, delete_raffles, detail_raffles, order_payment, order_reset


urlpatterns = [
    path("", list_raffles, name="list-raffles"),
    path("add/", add_raffles, name="add-raffles"),
    path("<int:raffle_pk>/delete/", delete_raffles, name="delete-raffles"),
    path("<int:raffle_pk>/detail/", detail_raffles, name="detail-raffles"),
    path("order/<int:order_pk>/pay/", order_payment, name="pay-order"),
    path("order/<int:order_pk>/reset/", order_reset, name="reset-order"),
]
