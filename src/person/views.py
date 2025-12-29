from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def index(request):
	return render(request, 'person/index.html')


def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			next_url = request.GET.get('next') or request.POST.get('next') or 'index'
			return redirect(next_url)
	else:
		form = AuthenticationForm()

	return render(request, 'person/login.html', {'form': form})


def logout_view(request):
	logout(request)
	return redirect('index')
