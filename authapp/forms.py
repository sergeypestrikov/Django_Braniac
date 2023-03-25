from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


# Оформление формы (альтернатива crispy forms)
from django.core.exceptions import ValidationError


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            print(field.widget)
            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-basic'
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-time'
            elif isinstance(field.widget, forms.widgets.SelectMultiple):
                field.widget.attrs['class'] = 'select2 form-control select2-multiple'
            else:
                field.widget.attrs['class'] = 'form-control'


# Форма создания пользователя
class CustomUserCreationForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'age', 'email', 'avatar')

    # Валидация пользователя (если требуется)
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise ValidationError('Вы слишком молоды для этого сайта')
        return age


# Форма редактирования данных пользователя
class CustomUserChangeForm(StyleFormMixin, UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'age', 'email', 'avatar')

    # Валидация пользователя (если требуется)
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise ValidationError('Вы слишком молоды для этого сайта')
        return age
