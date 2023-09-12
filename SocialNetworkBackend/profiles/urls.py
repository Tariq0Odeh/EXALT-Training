from django.urls import path
from .views import CreateProfileView, EditProfileView, SearchProfileView


urlpatterns = [
    path('', CreateProfileView.as_view(), name="profile"),
    path('edit/', EditProfileView.as_view(), name="edit-profile"),
    path('search/', SearchProfileView.as_view(), name="search-profile"),
]