from ..models import Insurance


class InsuranceOptions:
    model = Insurance

    @classmethod
    def delete_user(cls, insurance_id):
        return cls.model.objects.filter(id=insurance_id).delete()