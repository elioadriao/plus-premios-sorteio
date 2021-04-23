from django.shortcuts import render, reverse, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required, user_passes_test

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
    form = RaffleForm(request.POST or None)

    if form.is_valid():
        raffle = form.save()
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
        quota = form.save(commit=False)
        Quota.objects.filter(
            raffle=raffle, number=quota.number
            ).update(status="reserved", owner=request.user)

        return redirect(reverse("raffles:detail-raffles", args=(raffle_pk,)))

    return render(request, "raffles/detail_raffles.html", context={"raffle": raffle, "form": form})
