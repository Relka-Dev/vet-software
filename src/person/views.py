from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from person.forms import PersonLoginForm


def index(request):
    return render(request, 'person/index.html')


def login_view(request):
    if request.method == 'POST':
        form = PersonLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authentification via votre backend personnalisé
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                next_url = request.GET.get('next') or request.POST.get('next') or 'index'
                return redirect(next_url)
            else:
                form.add_error(None, "Email ou mot de passe incorrect")
    else:
        form = PersonLoginForm()

    return render(request, 'person/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')
