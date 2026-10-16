from django import forms
from .models import Product
from .constants import FORBIDDEN_WORDS

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']  # подстрой под свои поля
        # если у тебя есть поле is_active (чекбокс), оставь его — оно автоматически станет чекбоксом

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Задание 3: стилизация через __init__
        for field_name, field in self.fields.items():
            # Для всех текстовых полей ставим класс form-control
            if isinstance(field, forms.CharField) or isinstance(field, forms.DecimalField):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.label  # опционально: подсказка-плейсхолдер
                })
            # Для чекбоксов (например, is_active) — отдельный стиль
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form-check-input'})

    # Задание 1: проверка на запрещённые слова
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            return name
        name_lower = name.lower()
        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise forms.ValidationError(f'В названии нельзя использовать слово "{word}".')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            return description
        desc_lower = description.lower()
        for word in FORBIDDEN_WORDS:
            if word in desc_lower:
                raise forms.ValidationError(f'В описании нельзя использовать слово "{word}".')
        return description

    # Задание 2: кастомная валидация цены (не отрицательная)
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной.')
        return price
