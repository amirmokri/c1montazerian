from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    phone_number = forms.CharField(
        max_length=15,
        label="شماره تلفن",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = User
        fields = ["username", "phone_number", "password1", "password2"]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data["phone_number"]
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data["phone_number"]
            )
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="نام کاربری",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

