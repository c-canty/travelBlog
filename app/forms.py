"""
Definition of forms.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from pycountry import countries
from .models import BlogEntry

COUNTRY_CHOICES = [(country.alpha_2, country.name) for country in countries]

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class BlogEntryCreateForm(forms.ModelForm):
    class Meta:
        model = BlogEntry
        fields = ['title', 'body', 'city', 'country', 'active']  # Include required fields
        widgets = {
            'title': forms.TextInput({
                'class': 'form-control',
                'placeholder': 'Title',
            }),
            'body': forms.Textarea({
                'class': 'form-control',
                'placeholder': 'Body',
            }),
            'city': forms.TextInput({
                'class': 'form-control',
                'placeholder': 'City',
            }),
            'country': forms.Select(  # Use a Select widget with country choices
                choices=COUNTRY_CHOICES,
                attrs={
                    'class': 'form-control',
                },
            ),
            'active': forms.CheckboxInput({
                'class': 'form-control',
            }),
        }




class BlogEntryUpdateForm(forms.ModelForm):
    class Meta:
        model = BlogEntry
        fields = ['title', 'body', 'city', 'country', 'active']
        widgets = {
            'title': forms.TextInput({
                'class': 'form-control',
                'placeholder': 'Title',
            }),
            'body': forms.Textarea({
                'class': 'form-control',
                'placeholder': 'Body',
            }),
            'city': forms.TextInput({
                'class': 'form-control',
                'placeholder': 'City',
            }),
            'country': forms.Select(
                choices=COUNTRY_CHOICES,  # Use the same choices
                attrs={
                    'class': 'form-control',
                },
            ),
            'active': forms.CheckboxInput({
                'class': 'form-control',
            }),
        }



class BlogEntryDeactivateForm(forms.ModelForm):
    class Meta:
        model = BlogEntry
        fields = ['active']  # Only include the 'active' field
        widgets = {
            'active': forms.CheckboxInput({
                'class': 'form-control',
            }),
        }

    

