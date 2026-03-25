from django import forms
from .models import Product, ReviewRating


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'slug',
            'description',
            'price',
            'images',
            'is_available',
            'category',
        ]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['product_name'].widget.attrs['class'] = 'form-control'
        self.fields['product_name'].widget.attrs['placeholder'] = 'Enter Product Name'

        self.fields['slug'].widget.attrs['class'] = 'form-control'
        self.fields['slug'].widget.attrs['placeholder'] = 'Enter Product Slug'

        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Product Description'
        self.fields['description'].widget.attrs['rows'] = 4

        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['placeholder'] = 'Enter Price'

        self.fields['images'].widget.attrs['class'] = 'form-control'

        self.fields['is_available'].widget.attrs['class'] = 'form-check-input'

        self.fields['category'].widget.attrs['class'] = 'form-control'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter review title',
            }),
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your review here',
                'rows': 4,
            }),
            'rating': forms.Select(
                choices=[
                    ('', 'Select Rating'),
                    (1, '1 Star'),
                    (2, '2 Stars'),
                    (3, '3 Stars'),
                    (4, '4 Stars'),
                    (5, '5 Stars'),
                ],
                attrs={'class': 'form-control'}
            ),
        }