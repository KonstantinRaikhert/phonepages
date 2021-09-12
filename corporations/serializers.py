from django.db.models import Q
from rest_framework import serializers

from corporations.models import Employee, Firm, Phone, Profession


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"


class FirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = "__all__"


class PhoneSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = "__all__"

    def to_representation(self, instance):
        return {"phone": "{}: {}".format(instance.type, instance.phone_number)}


class EmployeeSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

    def to_representation(self, instance):
        phone = PhoneSearchSerializer(instance.phone.all(), many=True)
        employee = {
            "id": instance.id,
            "employee": {
                "info": "{} {} {} ({})".format(
                    instance.last_name,
                    instance.first_name,
                    instance.middle_name,
                    instance.profession.profession,
                ),
                "contact": [phone.data],
            },
        }
        return employee


class FirmSearchSerializer(serializers.ModelSerializer):
    employees = serializers.SerializerMethodField()

    class Meta:
        model = Firm
        fields = ["id", "name", "employees"]

    def get_employees(self, obj):
        request = self.context.get("request")
        search = request.query_params.get("search")
        if search is not None:
            return EmployeeSearchSerializer(
                obj.employees.filter(
                    Q(first_name__icontains=search)
                    | Q(last_name__icontains=search)
                    | Q(middle_name__icontains=search)
                    | Q(profession__profession__icontains=search)
                    | Q(phone__phone_number__icontains=search)
                ).distinct()[:5],
                many=True,
            ).data
        return EmployeeSearchSerializer(
            obj.employees.distinct()[:5], many=True
        ).data


class PhoneNumberSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()

    class Meta:
        model = Phone
        fields = [
            "type",
            "phone_number",
        ]

    def validate(self, data):
        request = self.context.get("request")

        if request.method == "POST":
            type = data.get("type")
            phone_number = data.get("phone_number")
            if type == Phone.PhoneType.PERSONAL:
                used = Phone.objects.filter(
                    type=type,
                    number=phone_number,
                ).exists()
                if used:
                    raise serializers.ValidationError(
                        "Этот личный номер уже используется"
                    )
            if phone_number[0] != "+":
                raise serializers.ValidationError(
                    "Номер должен начинаться с +"
                )
        return data


class EmployeesSerializer(serializers.ModelSerializer):
    phone = PhoneNumberSerializer(many=True)
    profession = ProfessionSerializer()
    full_name = serializers.SerializerMethodField()

    class Meta:
        fields = fields = [
            "id",
            "full_name",
            "profession",
            "firm",
            "phone",
        ]
        model = Employee

    def get_full_name(self, obj):
        return "{} {} {}".format(
            obj.first_name, obj.middle_name, obj.last_name
        )

    def validate(self, data):
        request = self.context.get("request")
        if request.method in ("POST", "PUT", "PATCH"):
            full_name = data["full_name"].splite()
            firm = data["firm"]
            phone = data["phone"]
            person_in_firm = Employee.objects.filter(
                first_name=full_name[0],
                middle_name=full_name[1],
                last_name=full_name[2],
                firm=firm,
            ).exists()
            if person_in_firm:
                raise serializers.ValidationError(
                    "Сотрудник с таким именем уже есть в этой компании."
                )
            if not phone:
                raise serializers.ValidationError(
                    "Необходимо указать номер(номера) сотрудника"
                )
        return data


class IsCreatorSerializer(serializers.Serializer):
    user = serializers.ListField(child=serializers.EmailField())
