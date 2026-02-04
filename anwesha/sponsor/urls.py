from django.urls import path
from .views import allsponsors, MyntraStatus

sponsor_urls = [
    path("allsponsors", allsponsors, name="alluser"),
    path("myntra-status/", MyntraStatus.as_view(), name="myntra_status"),
]
