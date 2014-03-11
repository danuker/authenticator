from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

@login_required
def home(request):
    return render(request, 'home.html', {'username':request.user.first_name})

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return redirect('/login/')


@csrf_protect
def login(request):
    if request.user.is_authenticated():
        return redirect('/')

    elif request.method == 'POST':
        user = auth.authenticate(email=request.POST['email'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            print("User is valid and authenticated")
        else:
            print("The username and password were incorrect.")
        return redirect('/')

    elif request.method == 'GET':
        c = {}
        c.update(csrf(request))
        return render(request, 'login.html', c)