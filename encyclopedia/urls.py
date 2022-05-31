from django.urls import path

from . import views

app_name= "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.display_entry, name="entry"),
    path("wiki/edit/<str:entry>", views.edit, name="edit"),
    path("wiki/search/<str:keyword>", views.search, name="search"),
    path("new", views.new, name="new"),
    path("random", views.random, name="random")
]
