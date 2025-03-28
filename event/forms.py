from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from event.models import Accommodation, Food,Contact


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class AccommodationForm(forms.ModelForm):  # Inherit from forms.ModelForm
    arrival_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Arrival Time (YYYY-MM-DD HH:MM)'}))

    class Meta:
        model = Accommodation
        fields = ('first_name', 'last_name', 'email','type_accommodation', 'arrival_time', 'stay_length', 'additional_information')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'type_accommodation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'type_accommodation'}),
            'stay_length': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stay Length (days)'}),
            'additional_information': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional Information'}),
        }



class FoodForm(forms.ModelForm):
    pickup_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Pickup Time (HH:MM)'}))
    require_delivery = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Delivery Address (if required specify address)'}))

    class Meta:
        model = Food
        fields = ('full_name', 'email', 'type_food', 'pickup_time', 'require_delivery', 'additional1_information')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'type_food': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type of Food'}),
            'additional1_information': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional Information'}),
        }

class PaymentForm(forms.Form):
    phone_number = forms.CharField(
        label='Phone number',
        max_length=12,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    amount = forms.DecimalField(
        label='Amount (KES)',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class ContactForms(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }
