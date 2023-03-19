from django import forms
from .models import *


class ProductPublishForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'title',
            'description',
            'price',
            'shipping_fee',
            'returnable',
            'condition',
        )


class BidPublishForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = (
            'price',
        )