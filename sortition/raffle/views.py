from django.shortcuts import render, reverse, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required, user_passes_test

from django.utils import timezone

from django.core.paginator import Paginator

from .models import Raffle, Quota
from .forms import RaffleForm, QuotaForm


def list_raffles(request):
    paginator = Paginator(Raffle.objects.all().order_by("-date"), 3)

    page_number = request.GET.get("page")
    raffles_page_result = paginator.get_page(page_number)

    return render(
        request,
        "raffles/list_raffles.html",
        {"current_page": "raffles", "raffles_page_result": raffles_page_result},
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_raffles(request):
    form = RaffleForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        raffle = form.save(commit=False)
        raffle.created_by = request.user
        raffle.save()
        objs = (Quota(raffle=raffle, number=i+1) for i in range(raffle.quotas))
        Quota.objects.bulk_create(objs)

        return redirect(reverse("raffles:list-raffles"))

    return render(
        request,
        "raffles/add_raffles.html",
        context={
            "form": form,
        }
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_raffles(request, raffle_pk=None):
    raffle = get_object_or_404(Raffle.objects, pk=raffle_pk)
    raffle.delete()

    return redirect(reverse("raffles:list-raffles"))


@login_required
def detail_raffles(request, raffle_pk=None):
    raffle = get_object_or_404(Raffle.objects, pk=raffle_pk)
    form = QuotaForm(request.POST or None)

    if form.is_valid():
        form_quota = form.save(commit=False)
        quota = get_object_or_404(Quota.objects, raffle=raffle, number=form_quota.number)
        if quota.status == "open":
            quota.status = "reserved"
            quota.owner = request.user
            quota.reserved_at = timezone.now()
        quota.save()

        return redirect(reverse("raffles:detail-raffles", args=(raffle_pk,)))

    return render(
        request, "raffles/detail_raffles.html",
        context={"raffle": raffle, "form": form, "quotas": raffle.quota_set.all().order_by("number")}
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def quota_payment(request, quota_pk=None):
    quota = get_object_or_404(Quota.objects, pk=quota_pk)
    if quota.status == "reserved":
        quota.status = "paid"
        quota.paid_at = timezone.now()
        quota.save()

    return redirect("account:detail-users")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def quota_reset(request, quota_pk=None):
    quota = get_object_or_404(Quota.objects, pk=quota_pk)
    if quota.status == "reserved":
        quota.status = "open"
        quota.owner = None
        quota.reserved_at = None
        quota.paid_at = None
        quota.save()

    return redirect("account:detail-users")
