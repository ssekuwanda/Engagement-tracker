from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST) # form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request,' Signup successful, Welcome to the Tracker')
            return redirect('/')
        else:
            messages.warning(request, 'Please fill in all the fields correctly')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
