import datetime
from django import forms


class UserLogin(forms.Form):
    email = forms.CharField(max_length=30, label='Введите email')
    password = forms.CharField(max_length=15, label='Введите пароль')


class UserRegister(forms.Form):
    email = forms.CharField(max_length=30, label='Введите email')
    password = forms.CharField(max_length=15, label='Введите пароль')
    repeat_password = forms.CharField(min_length=8, label='Повторите пароль')


class UserProfileForm(forms.Form):
    name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    age = forms.IntegerField(max_value=100)
    email = forms.CharField(max_length=100)


class DateTimeForm(forms.Form):
    date_time = forms.DateTimeField(required=False, widget=forms.DateInput(attrs={'type': 'datetime-local'}),
                                     initial=datetime.date.today(), localize=True)