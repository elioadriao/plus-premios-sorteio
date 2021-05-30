from django.shortcuts import render, reverse, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required, user_passes_test

from django.utils import timezone

from .models import Raffle, Quota
from .forms import RaffleForm, QuotaForm, WinnerForm


def list_raffles(request):
    raffles_result = Raffle.objects.all().order_by("-date")
    winners_result = raffles_result.exclude(winner__isnull=True)

    return render(
        request,
        "raffles/list_raffles.html",
        {
            "current_page": "raffles", "raffles_result": raffles_result,
            "winners_result": winners_result
        },
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
    quotas_result = raffle.quota_set.all().order_by("number")
    quota_form = QuotaForm(request.POST or None, raffle_pk=raffle.id)

    if quota_form.is_valid():
        if raffle.is_date_valid():
            quotas = quota_form.cleaned_data["quotas"]
            for quota in quotas:
                if quota.status == "open":
                    quota.status = "reserved"
                    quota.owner = request.user
                    quota.reserved_at = timezone.now()
            Quota.objects.bulk_update(quotas, ["status", "owner", "reserved_at"])

        return redirect(reverse("raffles:detail-raffles", args=(raffle_pk,)))

    winner_form = WinnerForm(request.POST or None)

    if winner_form.is_valid():
        winner_quota_id = winner_form.cleaned_data["winner_quota_id"]
        sorted_quota = winner_form.cleaned_data["sorted_quota"]
        quota = get_object_or_404(Quota.objects, pk=winner_quota_id)

        raffle.winner = quota.owner
        raffle.sorted_quota = sorted_quota
        raffle.save()

        return redirect(reverse("raffles:detail-raffles", args=(raffle_pk,)))

    return render(
        request, "raffles/detail_raffles.html",
        context={
            "raffle": raffle, "quota_form": quota_form,
            "winner_form": winner_form, "quotas_result": quotas_result
        }
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
