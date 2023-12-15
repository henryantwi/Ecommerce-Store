from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)
from phonenumber_field.formfields import PhoneNumberField

from .models import UserBase



class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'example@nesttop.com', 'id': 'login-username', 'autofocus': 'autofocus'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Username (can not be changed)', min_length=3, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-username', 'readonly': 'readonly'}))

    full_name = forms.CharField(
        label='Fullname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Kennedy Agyapong', 'id': 'form-fullname', 'autofocus': 'autofocus'}))
    
    phone_number = forms.CharField(
        label='Phone Number', min_length=10, max_length=13, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Phone Number', 'id': 'form-phonenumber'}))
    
    

    class Meta:
        model = UserBase
        fields = ('email', 'user_name', 'full_name', 'phone_number',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user


class RegistrationForm(forms.ModelForm):

    user_name = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    full_name = forms.CharField(label='Enter Fullname', min_length=4, max_length=50, help_text='Required')
    phone_number = PhoneNumberField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email', 'full_name', 'phone_number',)

    def clean_user_name(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username', 'autofocus': 'autofocus'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Email', 'name': 'email', 'id': 'id_email'})
        self.fields['full_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Fullname'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Phone Number'})


class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Confirm Password', 'id': 'form-new-pass2'}))