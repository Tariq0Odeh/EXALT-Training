from django.urls import path
from .views import CreateProfileView, EditProfileView, SearchProfileView

urlpatterns = [
    path('create/', CreateProfileView.as_view(), name="create-profile"),
    path('edit/', EditProfileView.as_view(), name="edit-profile"),
    path('', SearchProfileView.as_view(), name="search-profile"),
]