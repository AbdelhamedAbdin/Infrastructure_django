from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, Role


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'
    }), label='password')
    password2 = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }), label='Confirm Password')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'roles', 'password1']
        widgets = {
            'roles': forms.CheckboxSelectMultiple()
        }

    def clean_password2(self):
        password = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password and password2 and password != password2:
            raise forms.ValidationError("password and confirm password is not same")
        if len(password) < 4:
            raise forms.ValidationError('Password is very weak please enter 4 words at least')
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.staff = True
            user.set_password(self.cleaned_data['password1'])
            user.save()
            user.roles.add(*self.cleaned_data['roles'])
        return user
