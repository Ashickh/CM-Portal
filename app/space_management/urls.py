from django.urls import path
from .views import * 
urlpatterns = [
    path("country/",CountryView.as_view()),
    path("state/",StateView.as_view()),
    path("city/",CityView.as_view()),
    path("city/<int:id>/",CityUpdateDelete.as_view()),
    path("building/",Building.as_view()),
    path("building/<int:id>/",BuildingDeleteUpdate.as_view()),
    path("space/",RentalSpaceView.as_view()),
    path("space/<int:id>/",RentalSpaceUpdateDelete.as_view()),

    path("spacenotification/",SpaceNotificationView.as_view()),

    path("customerbuildingddropdown/",CustomerBuildingDropdown.as_view()),
    path("customerspaceddropdown/",CustomerSpaceDropdown.as_view()),
   
]
