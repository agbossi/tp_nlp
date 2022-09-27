from django.conf.urls import url
from django.urls import path

from tp_nlp_app import views

urlpatterns = [
    url(r'^api/summary$', views.place_summary),
    url(r'^api/places$', views.places),
    url(r'^api/places/entry', views.place_entry),
    path("api/places/<str:placeId>", views.place),
    path("api/places/<str:placeId>/blacklist", views.blacklist)
]
