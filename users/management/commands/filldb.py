import factory
from django.core.management.base import BaseCommand

from users.factories import UserFactory


class AllFactories:
    def create_users_default(self, arg):
        UserFactory.create_batch(arg)

    def create_users_is_staff(self, arg):
        for _ in range(arg):
            UserFactory.create(is_staff=True)

    def create_users_no_active(self, arg):
        for _ in range(arg):
            UserFactory._create(is_active=False)


all_factories = AllFactories()

OPTIONS_AND_FUNCTIONS = {
    "users_default": all_factories.create_users_default,
    "users_admin": all_factories.create_users_is_staff,
    "users_no_active": all_factories.create_users_no_active,
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
                    # if Recipe.objects.count() > 10:
                    #     raise MyException()
                    UserFactory.create_batch(5)

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
