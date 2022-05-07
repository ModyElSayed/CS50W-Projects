from django.urls import path
from . import views

app_name = 'wiki'

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_title>", views.title, name="title"),
    path("search", views.search, name="search"),
    path("new-page", views.new_page, name="new_page"),
    path("edit-page", views.edit_page, name="edit_page"),
]
