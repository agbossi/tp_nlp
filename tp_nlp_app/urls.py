from django.conf.urls import url
from tp_nlp_app import views

urlpatterns = [
    url(r'^api/summary$', views.place_summary),
    url(r'^api/places$', views.places),
    url(r'^api/places/entry', views.place_entry)
]
