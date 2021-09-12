from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy
from phone_field import PhoneField

from users.models import AdvancedUser


class Phone(models.Model):
    class PhoneType(models.TextChoices):
        OFFICE = "Office phone", gettext_lazy("Рабочий")
        PERSONAL = "Personal phone", gettext_lazy("Личный")
        FAX = "Fax phone", gettext_lazy("Факс")

    phone_number = PhoneField(
        help_text="Телефонный номер", verbose_name="Телефонный номер"
    )
    type = models.CharField(
        verbose_name="Тип номера", max_length=15, choices=PhoneType.choices
    )

    class Meta:
        verbose_name = "Телефонный номер"
        verbose_name_plural = "Телефонные номера"

    def __str__(self):
        return f"{self.type} - {self.phone_number}"


class Profession(models.Model):
    profession = models.CharField(
        verbose_name="Должность", max_length=150, unique=True
    )

    class Meta:
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"
        ordering = ["profession"]

    def __str__(self):
        return self.profession


class Firm(models.Model):
    name = models.CharField(
        verbose_name="Название компании", max_length=50, unique=True
    )
    address = models.CharField(verbose_name="Адрес", max_length=100)
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(verbose_name="Имя", max_length=50)
    last_name = models.CharField(verbose_name="Фамилия", max_length=50)
    middle_name = models.CharField(verbose_name="Отчество", max_length=50)
    firm = models.ForeignKey(
        Firm,
        on_delete=models.PROTECT,
        related_name="employees",
        verbose_name="Компания",
    )
    profession = models.ForeignKey(
        Profession,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Должность",
    )
    phone = models.ManyToManyField(
        Phone, related_name="employees", blank=False, verbose_name="Телефоны"
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["firm"]

    def __str__(self):
        return "{} {} {}".format(
            self.first_name, self.last_name, self.middle_name
        )

    def clean(self):
        employee = Employee.objects.filter(
            first_name=self.first_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
            firm=self.firm,
        )
        if employee:
            raise ValidationError(
                "Сотрудник уже зарегистрирован в этой компании"
            )


class UserFirm(models.Model):
    user = models.ForeignKey(
        AdvancedUser, on_delete=models.PROTECT, verbose_name="Пользователь"
    )
    firm = models.ForeignKey(
        Firm, on_delete=models.PROTECT, verbose_name="Компания"
    )
    is_create = models.BooleanField(
        default=False, verbose_name="Администратор"
    )

    class Meta:
        verbose_name = "Компания пользователя"
        verbose_name_plural = "Компании пользователья"
        ordering = ["firm"]

    def __str__(self):
        return f"{self.user} - {self.firm}"
