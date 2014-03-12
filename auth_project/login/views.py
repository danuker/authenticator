from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from models import User


@login_required
def home(request, message=None):
    return render(request, 'home.html', {'name': request.user.get_short_name(),
                                         'message': message,
                                         'is_verified': request.user.is_verified,
    })


@login_required
def user_logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return redirect('/login/')


@csrf_protect
def user_login(request, message=None):
    if request.user.is_authenticated():
        return redirect('/', message="Already logged in!")

    elif request.method == 'GET':
        c = {}
        c.update(csrf(request))
        c['message'] = message
        return render(request, 'login.html', c)

    elif request.method == 'POST':
        user = auth.authenticate(email=request.POST['email'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            print("User is valid and authenticated")
        else:
            print("The username and password were incorrect.")
            return redirect('/login/', message="Invalid credentials.")
        return redirect('/')


def user_register(request):
    if request.user.is_authenticated():
        return redirect('/')
    elif request.method == 'GET':
        # Show the registration form
        return render(request, 'register.html')

    elif request.method == 'POST':
        # Register the user, if valid credentials

        u = User.objects.create_user(email=request.POST['email'],
                                     first_name=request.POST['first-name'],
                                     last_name=request.POST['last-name'],
                                     web_url=request.POST['web-url'],
        )
        u.set_password(request.POST['password'])
        u.save()
        return redirect('/login/')


@login_required
def user_validate(request):
    if request.method == 'GET':
        # TODO: Send an email to check the user's address
        # TODO: Allow get params directly from email (Special case if they exist)
        return render(request, 'email_send.html',
                      {'name': request.user.get_short_name(),
                       'email': request.user.email
                      })
    elif request.method == 'POST':
        # Check if the code is proper (????)
        if request.POST['code'] == request.user.email:  # TODO: use an actual code
            # The user is verified
            request.user.is_verified = True
            request.user.save()
        return redirect('/')

