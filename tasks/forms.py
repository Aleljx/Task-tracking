from django import forms
from tasks.models import Task
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Неправильний логін або пароль!",
        "inactive": "Цей акаунт деактивований.",
    }
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Ім'я користувача",
        help_text="Може містити до 150 символів. Літери, цифри та символи @/./+/-/_",
    )
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="Мінімум 8 символів. Не використовуйте занадто прості паролі.",
    )
    password2 = forms.CharField(
        label="Підтвердження пароля",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text="Введіть той самий пароль ще раз.",
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status','priority', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date',})
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields["due_date"].widget.attrs["class"] += ' my-custom=datepicker'

class TaskFilterForm(forms.Form):
    STATUS_CHOICES = (
        ("", "Всі"),
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Статус")

    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)
        self.fields["status"].widget.attrs.update({'class': 'form-control'})
