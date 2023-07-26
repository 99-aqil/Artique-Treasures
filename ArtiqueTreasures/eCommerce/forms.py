from django import forms
from .models import Product

class AdminProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('status',)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'description', 'price', 'image')
