import json
from api_insurances import models
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load insurers data"

    def handle(self, *args, **kwargs):
        json_data = open('api_insurances/fixtures/aseguradoras.json')
        insurance_data = json.load(json_data)

        for insurance in insurance_data:
            insurance_queryset = models.Insurers.objects.filter(id=insurance.get("id"))
            if not insurance_queryset:
                print(insurance)
                models.Insurers(**insurance).save()
        json_data.close()