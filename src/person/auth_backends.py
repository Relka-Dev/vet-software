from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from person.models import Person

class PersonAuthBackend(BaseBackend):
    """
    Authentifie les utilisateurs via la table Person
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            person = Person.objects.get(email=username)

            if check_password(password, person.password_hash):
                return person
        except Person.DoesNotExist:
            return None

        return None

    def get_user(self, user_id):
        try:
            return Person.objects.get(pk=user_id)
        except Person.DoesNotExist:
            return None
