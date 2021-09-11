from django.urls import include, path
from rest_framework.routers import DefaultRouter

from corporations.views import EmployeeViewSet, FirmViewSet, ProfessionViewSet

router = DefaultRouter()

router.register("organizations", FirmViewSet, basename="organizations")
router.register("positions", ProfessionViewSet, basename="positions")
router.register(
    r"organizations/(?P<org_id>\d+)/employees",
    EmployeeViewSet,
    basename="employees",
)


urlpatterns = [
    path("", include(router.urls)),
]
