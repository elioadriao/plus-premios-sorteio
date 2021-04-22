from django.shortcuts import render, reverse, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.paginator import Paginator

from .models import Raffle
from .forms import RaffleForm


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
        form.save()
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

    return render(request, "raffles/detail_raffles.html", context={"raffle": raffle})
