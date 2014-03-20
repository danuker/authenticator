from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormView

from forms import LoginForm, RegisterForm, ValidateForm, PWResetEmailForm


class HomeView(View, TemplateResponseMixin):
    template_name = 'home.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'user': request.user})


class UserLogout(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserLogout, self).dispatch(*args, **kwargs)

    def get(self, request):
        auth.logout(request)
        messages.success(request, "Logged out.")
        return redirect('/login/')


class UserLogin(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    redirect_field_name = auth.REDIRECT_FIELD_NAME
    success_url = '/'

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(UserLogin, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.authenticate_and_login(self.request)
        return super(UserLogin, self).form_valid(form)


class UserRegister(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        # create user
        user = form.save()
        return super(UserRegister, self).form_valid(form)


class UserValidate(FormView):
    template_name = 'email_send.html'
    form_class = ValidateForm
    success_url = '/'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(UserLogout, self).dispatch(*args, **kwargs)

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """

        # Generate a code
        self.request.session['code'] = str(abs(hash(self.request.user.email)))

        kwargs = self.get_form_kwargs()
        kwargs.update({'code': self.request.session['code'],
                       'email': self.request.user.email,
                       'name': self.request.user.get_short_name()})

        instance = form_class(**kwargs)

        # Send the email
        instance.send_email()

        return instance

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.request.user.is_verified = True
        self.request.user.save()
        messages.success(self.request, "Successfully verified email!")
        return super(UserValidate, self).form_valid(form)

    def form_invalid(self, form):
        return super(UserValidate, self).form_invalid(form)


class PWResetEmail(FormView):
    """
    Prompts for the email to reset
    """

    form_class = PWResetEmailForm
    template_name = 'pw_reset_email.html'
    success_url = '/reset_pw_code/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.request.user.is_verified = True
        self.request.user.save()
        messages.success(self.request, "E-mail sent if user exists.")
        return super(UserValidate, self).form_valid(form)


class PWResetResponse(FormView):
    """
    Prompts for the password
    """
    pass