from django.shortcuts import redirect
from django.contrib.auth import logout
from person.models import Person


class PersonAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_paths = ['/favicon.ico', '/static/', '/media/']

        if any(request.path.startswith(path) for path in excluded_paths):
            return self.get_response(request)

        # Si on est sur l'admin et que l'utilisateur est une Person, logout
        if request.path.startswith('/admin'):
            if request.user.is_authenticated and isinstance(request.user, Person):
                logout(request)
                # return redirect('person:login')
            return self.get_response(request)

        # Pour le reste du site, on check si l'utilisateur est connecté en tant que instance de person. Sinon, logout.
        if request.user.is_authenticated and not isinstance(request.user, Person):
            logout(request)
            # return redirect('person:login') # Si on veut la redirection si la personne est pas connectée

        return self.get_response(request)
