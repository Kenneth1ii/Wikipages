from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("<str:title>/editpage",views.editpage, name="editpage"),
    path("randoms", views.randoms, name="randoms"),
    path("<str:title>", views.entry, name="entry"),
]

