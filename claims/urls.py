from django.urls import path

from . import views

app_name = "claims"

urlpatterns = [
    path("<int:pk>/proof-photo/", views.proof_photo, name="proof_photo"),
    # US-07, US-08, US-11, US-17 go here
]
