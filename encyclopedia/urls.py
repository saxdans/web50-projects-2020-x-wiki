from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("createpage", views.createpage, name="createpage"),
    path("nosuchpage/<str:search>", views.noSuchPage, name="nosuchpage"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("editpage/<str:title>", views.edit, name="editpage"),
    path("random", views.randompage, name="random"),
    path("searchresults/<str:search>", views.searchResults, name="searchresults"),
    path("matchingresults", views.matches, name="matches")
]
