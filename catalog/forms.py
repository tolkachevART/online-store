from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, ModelForm

from catalog.models import Product, Version

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
                   'обман', 'полиция', 'радар']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name').lower()
        description = cleaned_data.get('description').lower()

        for word in FORBIDDEN_WORDS:
            if word in name or word in description:
                raise forms.ValidationError(f'Слово "{word}" запрещено')

        return cleaned_data


class StyleFormMixin:
    pass


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
