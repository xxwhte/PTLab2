from django import forms

from .models import Purchase


PROMO_DISCOUNTS = {'TOY5': 5, 'TOY10': 10, 'TOY15': 15}


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['person', 'address', 'promo_code']
        labels = {'person': 'Имя', 'address': 'Адрес доставки'}
        help_texts = {'promo_code': 'Можно оставить пустым'}

    def clean_promo_code(self):
        code = self.cleaned_data['promo_code'].upper()
        if code and code not in PROMO_DISCOUNTS:
            raise forms.ValidationError('Такого промокода нет.')
        return code
