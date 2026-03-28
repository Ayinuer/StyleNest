from django import forms
from .models import Subscriber


class SubscriberForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your phone number'
        })
    )

    class Meta:
        model = Subscriber
        fields = ['phone_number', 'birth_month']
        widgets = {
            'birth_month': forms.Select(attrs={'class': 'form-select form-select-lg'})
        }


class UnsubscribeForm(forms.Form):
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your phone number'
        })
    )