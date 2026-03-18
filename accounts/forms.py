from django import forms
from .models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Password',
            'class': 'form-control',
        })
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control',
        })
    )

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Password does not match!')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Enter First Name',
            'class': 'form-control',
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Enter Last Name',
            'class': 'form-control',
        })
        self.fields['phone_number'].widget.attrs.update({
            'placeholder': 'Enter Phone Number',
            'class': 'form-control',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter Email Address',
            'class': 'form-control',
        })


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Enter First Name',
            'class': 'form-control',
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Enter Last Name',
            'class': 'form-control',
        })
        self.fields['phone_number'].widget.attrs.update({
            'placeholder': 'Enter Phone Number',
            'class': 'form-control',
        })


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False,
        error_messages={'invalid': 'Image files only'},
        widget=forms.FileInput(attrs={
            'class': 'form-control',
        })
    )

    class Meta:
        model = UserProfile
        fields = (
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'country',
            'profile_picture',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['address_line_1'].widget.attrs.update({
            'placeholder': 'Address Line 1',
            'class': 'form-control',
        })
        self.fields['address_line_2'].widget.attrs.update({
            'placeholder': 'Address Line 2',
            'class': 'form-control',
        })
        self.fields['city'].widget.attrs.update({
            'placeholder': 'City',
            'class': 'form-control',
        })
        self.fields['state'].widget.attrs.update({
            'placeholder': 'State',
            'class': 'form-control',
        })
        self.fields['country'].widget.attrs.update({
            'placeholder': 'Country',
            'class': 'form-control',
        })