from django.urls import include, path
from rest_framework.routers import DefaultRouter

from corporations.views import (
    EmployeeViewSet,
    FirmViewSet,
    IsCreatorToEditView,
    ProfessionViewSet,
)

router = DefaultRouter()

router.register("firms", FirmViewSet, basename="firms")
router.register("professions", ProfessionViewSet, basename="professions")
router.register(
    r"firms/(?P<firm_id>\d+)/employees",
    EmployeeViewSet,
    basename="employees",
)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "firms/<int:firm_id>/access_edit/",
        IsCreatorToEditView.as_view(),
    ),
]
