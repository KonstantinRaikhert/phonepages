from django.urls import include, path
from rest_framework.routers import DefaultRouter

from corporations.views import EmployeeViewSet, FirmViewSet, ProfessionViewSet

router = DefaultRouter()

router.register("firms", FirmViewSet, basename="firms")
router.register("professions", ProfessionViewSet, basename="professions")
router.register(
    r"firms/(?P<org_id>\d+)/employees",
    EmployeeViewSet,
    basename="employees",
)


urlpatterns = [
    path("", include(router.urls)),
]
