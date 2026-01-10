class PersonAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_paths = ['/favicon.ico', '/static/', '/media/']

        if any(request.path.startswith(path) for path in excluded_paths):
            request.person = None
            return self.get_response(request)

        # Si on est sur l'admin, ne pas ajouter de Person
        if request.path.startswith('/admin'):
            request.person = None
            return self.get_response(request)

        # Pour le reste du site, ajoute la Person liée au user
        person = None
        if request.user.is_authenticated:
            # Si le user a une Person liée, on la met
            person = getattr(request.user, 'person', None)
        request.person = person

        return self.get_response(request)
