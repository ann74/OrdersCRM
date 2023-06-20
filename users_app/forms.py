from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():

            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
                field.widget.attrs['label_class'] = 'form-check-label'
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-basic'
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs['class'] = 'form-control datepicker'
                field.widget.attrs['label_classes'] = 'form-label'
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-time'
            elif isinstance(field.widget, forms.widgets.SelectMultiple):
                field.widget.attrs['class'] = 'form-control select2 select2-multiple'
            elif isinstance(field.widget, forms.widgets.Select):
                field.widget.attrs['class'] = 'form-control select2'
            else:
                field.widget.attrs['class'] = 'form-control'

            if field_name == 'old_id':
                field.widget = forms.HiddenInput()


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    CLIENT = 'clients'
    MASTER = 'masters'

    ROLES = (
        (CLIENT, 'заказчик'),
        (MASTER, 'мастер'),
    )

    role = forms.ChoiceField(choices=ROLES, required=True, label='Кто ты')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super().save()
        user.groups.add(Group.objects.get(name=self.cleaned_data['role']))
        if commit:
            user.save()
        return user


