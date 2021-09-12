import factory
from faker import Faker

from corporations.models import (
    Employee,
    Firm,
    Phone,
    Profession,
    UserFirmRelation,
)
from users.models import AdvancedUser

fake = Faker()


class ProfessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profession
        django_get_or_create = ["profession"]

    profession = factory.Faker("job", locale="ru_RU")


class PhoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Phone
        django_get_or_create = ["phone_number"]

    phone_number = factory.LazyAttribute(lambda _: fake.phone_number())
    type = factory.Iterator(
        Phone.PhoneType.choices,
        getter=lambda choice: choice[0],
    )


class FirmFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Firm
        django_get_or_create = ["name"]

    name = factory.Faker("company", locale="ru_RU")
    address = factory.Faker("address", locale="ru_RU")
    description = factory.Faker("text", max_nb_chars=1000, locale="ru_RU")
    creator = factory.Iterator(AdvancedUser.objects.all())
    access_edit = factory.Iterator(AdvancedUser.objects.all())

    @factory.post_generation
    def access_edit(self, create, extracted, **kwargs):
        if not create:
            return

        users = AdvancedUser.objects.order_by("?")[:3]
        self.access_edit.add(*users)


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    first_name = factory.Faker("first_name", locale="ru_RU")
    last_name = factory.Faker("last_name", locale="ru_RU")
    middle_name = factory.Faker("middle_name", locale="ru_RU")
    firm = factory.Iterator(Firm.objects.all())
    profession = factory.Iterator(Profession.objects.all())

    @factory.post_generation
    def phone(self, create, extracted, **kwargs):
        if not create:
            return

        phones = Phone.objects.order_by("?")[:2]
        self.phone.add(*phones)


class UserFirmRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserFirmRelation
        django_get_or_create = ["user"]

    user = factory.Iterator(AdvancedUser.objects.all())
    firm = factory.Iterator(Firm.objects.all())
