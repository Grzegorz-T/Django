from django.shortcuts import render, redirect
import requests

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from .decorators import unauthenticated_user
from .forms import CreateUserForm
from django.contrib import messages


@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			print('tworzenie konta')
			Member.objects.create(
				member = user,
				nick = user.username,
				)
			messages.success(request, 'Account was created for ' + user)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'register.html', context)

@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')