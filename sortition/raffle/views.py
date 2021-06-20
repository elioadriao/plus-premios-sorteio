from django.shortcuts import render, reverse, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required, user_passes_test

from django.utils import timezone

from .models import Raffle, Quota, QuotaOrder
from .forms import RaffleForm, QuotaForm, WinnerForm, RaffleFilterForm


def about(request):
    return render(
        request,
        "raffles/about.html",
    )


def index(request):
    raffles_result = Raffle.objects.filter(winner__isnull=True).order_by("-date")
    winners_result = raffles_result.exclude(winner__isnull=True)

    return render(
        request,
        "raffles/index.html",
        context={"raffles_result": raffles_result, "winners_result": winners_result}
    )


def list_raffles(request):
    raffles_result = Raffle.objects.all().order_by("-date")
    filter_form = RaffleFilterForm(request.GET or None, initial={"status": "all"})

    if filter_form.is_valid():
        if filter_form.cleaned_data["status"] == "open":
            raffles_result = raffles_result.filter(winner__isnull=True, sorted_quota__isnull=True)
        elif filter_form.cleaned_data["status"] == "closed":
            raffles_result = raffles_result.filter(winner__isnull=False, sorted_quota__isnull=False)

    return render(
        request,
        "raffles/list_raffles.html",
        context={"raffles_result": raffles_result, "filter_form": filter_form}
    )


def list_winners(request):
    winners_result = Raffle.objects.filter(winner__isnull=False).order_by("winner")

    return render(
        request,
        "raffles/list_winners.html",
        context={"winners_result": winners_result}
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
        context={"form": form}
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
    quota_form = QuotaForm(request.POST or None, raffle_pk=raffle.id)

    if quota_form.is_valid():
        if raffle.is_buy_valid():
            quotas = quota_form.cleaned_data["quotas"]
            order_value = len(quotas) * raffle.get_quota_value()
            order = QuotaOrder.objects.create(owner=request.user, value=order_value)
            for quota in quotas:
                if not quota.order:
                    quota.order = order
            Quota.objects.bulk_update(quotas, ["order"])

            return redirect(reverse("raffles:link-order", args=(order.id,)))

        return redirect(reverse("raffles:detail-raffles", args=(raffle_pk,)))

    winner_form = WinnerForm(request.POST or None, raffle_pk=raffle.id)

    if winner_form.is_valid():
        quota = get_object_or_404(Quota.objects, pk=winner_form.cleaned_data["winner_quota_id"])
        raffle.winner = quota.order.owner
        raffle.sorted_quota = quota.number
        raffle.dump_orders()
        raffle.save()

        return redirect(reverse("raffles:detail-raffles", args=(raffle_pk,)))

    return render(
        request, "raffles/detail_raffles.html",
        context={
            "raffle": raffle, "quota_form": quota_form,
            "winner_form": winner_form,
            "quotas_result": raffle.quota_set.filter(order__isnull=True).order_by("number")
        }
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def order_payment(request, order_pk=None):
    order = get_object_or_404(QuotaOrder.objects, pk=order_pk)
    if order.status == "reserved":
        order.status = "paid"
        order.paid_at = timezone.now()
        order.save()

    return redirect("account:detail-users")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def order_reset(request, order_pk=None):
    order = get_object_or_404(QuotaOrder.objects, pk=order_pk)
    if order.status == "reserved":
        order.status = "open"
        order.owner = None
        order.reserved_at = None
        order.paid_at = None
        order.save()

    return redirect("account:detail-users")


@login_required
def order_link(request, order_pk=None):
    order = get_object_or_404(QuotaOrder.objects, pk=order_pk)

    return render(request, "raffles/order_link.html", {"order": order})
