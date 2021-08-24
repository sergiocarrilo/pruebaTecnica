from django.contrib.auth.models import User


class UserOperations:
    model = User

    @classmethod
    def delete_user(cls, user):
        return cls.model.objects.filter(id=user.id).delete()

    @classmethod
    def set_new_password(cls, data, user):
        old_password = data.get("old_password")
        if not user.check_password(old_password):
            raise Exception("Wrong old password")

        user.set_password(data.get("old_password"))
        user.save()