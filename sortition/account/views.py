from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from .models import User
from .forms import UserForm

from ..raffle.models import Quota


def login(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        user = form.get_user()
        auth_login(request, user)
        return redirect("index")
    return render(request, "account/login.html", context={"form": form})


def add_users(request):
    form = UserForm(request.POST or None, instance=User())
    if form.is_valid():
        user = form.save()
        auth_login(request, user)
        return redirect("index")
    return render(request, "account/add.html", context={"form": form})


@login_required
def logout(request):
    auth_logout(request)
    return redirect("index")


@login_required
def detail_users(request):
    user = get_object_or_404(User.objects, pk=request.user.id)
    paginator = Paginator(Quota.objects.filter(status="reserved").order_by("-reserved_at"), 20)

    page_number = request.GET.get("page")
    quotas_page_result = paginator.get_page(page_number)

    return render(
        request, "account/detail.html", context={"user": user, "quotas_page_result": quotas_page_result}
    )
