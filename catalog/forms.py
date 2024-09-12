from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, BooleanField

from catalog.models import Product, Version


class StyleFormMixin:
    """
    Класс для стилизации форм.
    Используется для добавления CSS классов к полям форм.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    """
    Класс формы для продуктов.
    Включает проверку на запрещенные слова в названии и описании продукта.
    """

    class Meta:
        model = Product
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name').lower()
        description = cleaned_data.get('description').lower()

        FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
                           'обман', 'полиция', 'радар']

        for word in FORBIDDEN_WORDS:
            if word in name or word in description:
                raise forms.ValidationError(f'Слово "{word}" запрещено')

        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ('version_number', 'version_name', 'is_current')


class BaseVersionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        current_count = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False) and form.cleaned_data.get('is_current', False):
                current_count += 1
        if current_count > 1:
            raise ValidationError("Можно выбрать только одну версию!")
