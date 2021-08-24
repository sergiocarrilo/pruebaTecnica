from django.db import models
from django.contrib.auth.models import User
from django_mysql import models as mysql_models
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


# Create your models here
class Insurance(models.Model):
    CAR = "Coche"
    MOTORBIKE = "Moto"
    INSURANCE_CATEGORIES = (
        (CAR, "Coche"),
        (MOTORBIKE, "Moto"),
    )

    MONTHLY = "Mensual"
    ANNUALY= "Anual"
    INSURANCE_PERIODICITY = (
        (MONTHLY, "Mensual"),
        (ANNUALY, "Anual"),
    )

    user = models.ForeignKey(User, related_name="insurance", on_delete=models.CASCADE)
    insurance_price = models.FloatField("Cantidad_seguro")
    insurance_category = models.CharField("Insurance_category", max_length=40, choices=INSURANCE_CATEGORIES)
    periodicity = models.CharField("periodicity",max_length=20, choices=INSURANCE_PERIODICITY)
    insurer = models.ForeignKey("Insurers", related_name="insurer", on_delete=models.CASCADE)
    detail = models.CharField("Detail", max_length=255, blank=True)
    coverage_end = models.DateField()


class Insurers(models.Model):
    CAR = "Coche"
    MOTORBIKE = "Moto"
    INSURANCE_CATEGORIES = (
        (CAR, "Coche"),
        (MOTORBIKE, "Moto"),
    )
    name = models.CharField("Name", max_length=255, blank=True)
    categories = mysql_models.ListTextField(
        base_field = models.CharField("Insurance_category", max_length=40, choices=INSURANCE_CATEGORIES),
        size=63
    )
    phone = models.CharField("Detail", max_length=20, blank=True)


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
