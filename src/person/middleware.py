from django.shortcuts import redirect
from django.contrib.auth import logout
from person.models import Person


class PersonAuthMiddleware:
    """
    Déconnexion automatique des utilisateur administrateur
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclure les appels admin
        excluded_paths = ['/admin/']

        # Si l'admin est connecté mais que c'est pas une instance du modèle person, on déconnecte
        if request.user.is_authenticated and not isinstance(request.user, Person):
            if not any(request.path.startswith(path) for path in excluded_paths):
                logout(request)
                return redirect('person:login')

        response = self.get_response(request)
        return response
