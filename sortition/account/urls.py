from django.urls import path
from .views import login, logout, add_users, detail_users


urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("add/", add_users, name="add-users"),
    path("details/", detail_users, name="detail-users"),
]
