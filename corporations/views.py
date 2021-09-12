from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import filters, status
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from corporations.models import Employee, Firm, Profession, UserFirmRelation
from corporations.permissions import (
    IsCreator,
    IsCreatorOrAccessToEdit,
    IsCreatorOrReadOnly,
)
from corporations.serializers import (
    EmployeesSerializer,
    FirmSearchSerializer,
    FirmSerializer,
    IsCreatorSerializer,
    ProfessionSerializer,
)
from users.models import AdvancedUser


class ProfessionViewSet(ListModelMixin, GenericViewSet):
    queryset = Profession.objects.all().order_by("profession")
    serializer_class = ProfessionSerializer


class FirmViewSet(ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer
    permission_classes = [IsCreatorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
        "employees__first_name",
        "employees__last_name",
        "employees__middle_name",
        "employees__profession__profession",
        "employees__phone__phone_number",
    ]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FirmSearchSerializer
        return FirmSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(creator=user)


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeesSerializer
    permission_classes = [IsCreatorOrAccessToEdit]
    queryset = Employee.objects.all()

    def get_queryset(self):
        firm_id = self.kwargs["firm_id"]
        firm = Firm.objects.get(pk=firm_id)
        return firm.employees.all()


class IsCreatorToEditView(APIView):
    permission_classes = [IsCreator]
    serializer_class = IsCreatorSerializer

    def get(self, request, firm_id):
        firm = get_object_or_404(
            Firm,
            id=firm_id,
        )
        return JsonResponse(
            [user.email for user in firm.access_edit.all()],
            safe=False,
            status=status.HTTP_200_OK,
        )

    def post(self, request, firm_id):
        serializer = IsCreatorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            firm = get_object_or_404(
                Firm,
                id=firm_id,
            )
            users = get_list_or_404(
                AdvancedUser, email__in=request.data["user"]
            )
            for user in users:
                firm.access_edit.add(user)
                firm.save()
            return JsonResponse(
                firm.access_list(),
                safe=False,
                status=status.HTTP_200_OK,
            )

    def delete(self, request, firm_id):
        serializer = IsCreatorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            firm = get_object_or_404(
                Firm,
                id=firm_id,
            )
            users = get_list_or_404(
                AdvancedUser, email__in=request.data["user"]
            )
            for user in users:
                access_edit = get_object_or_404(
                    UserFirmRelation,
                    firm=firm,
                    user=user,
                )
                access_edit.delete()
            return JsonResponse(
                firm.access_list(),
                safe=False,
                status=status.HTTP_200_OK,
            )
