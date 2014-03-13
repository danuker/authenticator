from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.mail import send_mail

from models import User


@login_required
def home(request):
    return render(request, 'home.html', {'user': request.user})


@login_required
def user_logout(request):
    auth.logout(request)
    messages.success(request, "Logged out.")
    return redirect('/login/')


@csrf_protect
def user_login(request):
    if request.user.is_authenticated():
        messages.error(request, "Already logged in!")
        return redirect('/')

    elif request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        user = auth.authenticate(email=request.POST['email'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect('/')

        else:
            messages.error(request, "The credentials were incorrect.")
            return redirect('/login/')


def user_register(request):
    if request.user.is_authenticated():
        messages.warning(request, "You have been logged out to register a new user.")
        return redirect('/logout/')

    elif request.method == 'GET':
        # Show the registration form
        return render(request, 'register.html')

    elif request.method == 'POST':
        # Check passwords
        if request.POST['password'] != request.POST['password-2']:
            messages.error(request, 'Passwords did not match.')
            return redirect('register.html')

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
        code = str(abs(hash(request.user.email)))
        request.session['code'] = code
        send_mail('Verify email', 'The code is: ' + str(code), 'no-reply@auth.com',
                  [request.user.email], fail_silently=False)
        print 'Code:', code

        # TODO: Allow get params directly from email (Special case if they exist)
        return render(request, 'email_send.html',
                      {'name': request.user.get_short_name(),
                       'email': request.user.email
                      })
    elif request.method == 'POST':
        if 'code' in request.session and \
                        request.POST['code'] == request.session['code']:
            print 'code is verified'
            # The user is verified
            request.user.is_verified = True
            request.user.save()
            messages.success(request, "E-mail verified!")
            return redirect('/')
        messages.error(request, "Code incorrect!")
        return redirect('/')
