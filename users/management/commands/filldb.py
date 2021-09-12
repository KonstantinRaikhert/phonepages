import random

import factory
from django.core.management.base import BaseCommand

from corporations.factories import (
    EmployeeFactory,
    FirmFactory,
    PhoneFactory,
    ProfessionFactory,
    UserFirmRelationFactory,
)
from corporations.models import Firm
from users.factories import UserFactory


class AllFactories:
    def create_users_default(self, arg):
        UserFactory.create_batch(arg)

    def create_users_is_staff(self, arg):
        for _ in range(arg):
            UserFactory.create(is_staff=True)

    def create_users_no_active(self, arg):
        for _ in range(arg):
            UserFactory.create(is_active=False)

    def create_professions(self, arg):
        for _ in range(arg):
            ProfessionFactory.create()

    def create_phones(self, arg):
        for _ in range(arg):
            PhoneFactory.create()

    def create_firms(self, arg):
        for _ in range(arg):
            FirmFactory.create()

    def create_employess(self, arg):
        for _ in range(arg):
            phones = random.randint(1, 3)
            EmployeeFactory(phone=phones)

    def create_creators(self, arg):
        for _ in range(arg):
            UserFirmRelationFactory.create()


all_factories = AllFactories()

OPTIONS_AND_FUNCTIONS = {
    "users_default": all_factories.create_users_default,
    "users_admin": all_factories.create_users_is_staff,
    "users_no_active": all_factories.create_users_no_active,
    "professions": all_factories.create_professions,
    "phones": all_factories.create_phones,
    "firms": all_factories.create_firms,
    "employess": all_factories.create_employess,
    "creators": all_factories.create_creators,
}


class MyException(Exception):
    pass


class Command(BaseCommand):
    help = "Fill Data Base with the test data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users_default",
            nargs=1,
            type=int,
            help="Creates Users default objects",
            required=False,
        )
        parser.add_argument(
            "--users_admin",
            nargs=1,
            type=int,
            help="Creates Users objects witn staff permissions",
            required=False,
        )
        parser.add_argument(
            "--users_no_active",
            nargs=1,
            type=int,
            help="Creates not active Users objects",
            required=False,
        )
        parser.add_argument(
            "--professions",
            nargs=1,
            type=int,
            help="Creates Profession objects",
            required=False,
        )
        parser.add_argument(
            "--phones",
            nargs=1,
            type=int,
            help="Creates Phone objects",
            required=False,
        )
        parser.add_argument(
            "--firms",
            nargs=1,
            type=int,
            help="Creates Firm objects",
            required=False,
        )
        parser.add_argument(
            "--employess",
            nargs=1,
            type=int,
            help="Creates Employess objects with phones",
            required=False,
        )
        parser.add_argument(
            "--creators",
            nargs=1,
            type=int,
            help="Creates creator of firm",
            required=False,
        )

    def handle(self, *args, **options):  # noqa

        optional_arguments = 0
        for item in list(OPTIONS_AND_FUNCTIONS):
            if options[item]:
                optional_arguments += 1
                with factory.Faker.override_default_locale("ru_RU"):
                    OPTIONS_AND_FUNCTIONS[item](options[item][0])
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"{options[item][0]} {item} created successfully"
                        )
                    )

        if optional_arguments == 0:
            try:
                with factory.Faker.override_default_locale("ru_RU"):
                    if Firm.objects.count() > 10:
                        raise MyException()
                    UserFactory.create_batch(30)
                    ProfessionFactory.create_batch(50)
                    PhoneFactory.create_batch(100)
                    FirmFactory.create_batch(30)
                    for _ in range(100):
                        phones = random.randint(1, 3)
                        EmployeeFactory(phone=phones)

                    self.stdout.write(
                        self.style.SUCCESS(
                            "The database is filled with test data"
                        )
                    )
            except MyException:
                self.stdout.write(
                    self.style.ERROR(
                        "The database is already filled with standard test "
                        "data. To top up individual tables, use the arguments."
                    )
                )
