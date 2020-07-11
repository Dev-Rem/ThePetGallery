from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from .models import Pet
from .forms import PetForm

# Create your views here.
def index(request):
    pets = Pet.objects.all()
    return render(request, "pet/index.html", {"pets": pets})


def create(request):
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            new_pet = form.save(commit=False)
            new_pet.user = request.user
            new_pet.save()
            return redirect("pet:index")
    else:
        form = PetForm()
    return render(request, "pet/create.html", {"form": form})


@require_http_methods(["GET", "POST"])
def view(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == "POST":
        pet.delete()
        return redirect("pet:index")
    return render(request, "pet/view.html", {"pet": pet})


def edit(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    form = PetForm(instance=pet)
    if request.method == "POST":
        form = PetForm(instance=pet, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("pet:index")
    else:
        form = PetForm(instance=pet)
    return render(request, "pet/edit.html", {"form": form})


def contact_us(request):
    return render(request, "pet/contact_us.html", {})
