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
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً 09123456789'})
    )

    class Meta:
        model = User
        fields = ["username", "phone_number", "password1", "password2"]

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not phone.isdigit() or len(phone) != 11:
            raise forms.ValidationError("📞 لطفاً شماره تلفن معتبر ۱۱ رقمی وارد کنید.")
        if UserProfile.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("🚨 این شماره تلفن قبلاً ثبت شده است!")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(user=user, phone_number=self.cleaned_data["phone_number"])
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
