from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# placeholder: Browse listings (US-04, US-06)
@login_required
def home(request):
    return render(request, "listings/home.html")
