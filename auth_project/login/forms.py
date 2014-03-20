from django import forms
from django.contrib import auth, messages
from django.core.mail import send_mail

from models import User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def authenticate_and_login(self, request):

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Successfully logged in!")
        else:
            messages.error(request, "The credentials were incorrect.")

        return user


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, required=False, widget=forms.PasswordInput(), label=u'Confirm Password')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password2', 'web_url')
        widgets = {
            'password': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

    # TODO: ARGH!
    # If you define this, call super too! Else, no unique validation
    # def clean(self):
    #     raise forms.ValidationError("Email is not unique!")

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            print 'Passwords do not match!', password, password2
            raise forms.ValidationError('Passwords do not match!')
        return cleaned_data

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ValidateForm(forms.Form):
    """
    Form for validating the email
    """

    code_field = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.code = kwargs.pop('code')
        self.email = kwargs.pop('email')
        self.name = kwargs.pop('name')
        super(ValidateForm, self).__init__(*args, **kwargs)

    def send_email(self):
        send_mail('Verify email', 'The code is: ' + str(self.code), 'no-reply@auth.com',
                  [self.email], fail_silently=False)

    def clean(self):
        if self.cleaned_data.get('code_field') != self.code:
            raise forms.ValidationError("Invalid code!")


class PWResetEmailForm(forms.Form):
    email_field = forms.EmailField(label='E-mail')

    def send_email(self):
        send_mail('Reset password', 'The code is: ' + str(self.code), 'no-reply@auth.com',
                  [self.email_field], fail_silently=False)