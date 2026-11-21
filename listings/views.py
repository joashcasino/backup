from django.shortcuts import render

# placeholder
def home(request):
    return render(request, "listings/home.html")