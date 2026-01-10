from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from person.models import Person
from django.contrib.auth.models import User


class PersonAuthBackend(BaseBackend):
    """
    Authentifie les utilisateurs via la table Person
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            person = Person.objects.get(email=username)
            if check_password(password, person.password_hash):
                return person.user if person.user else None
        except Person.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
