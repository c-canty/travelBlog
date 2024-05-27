"""
Definition of forms.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from pycountry import countries
from .models import BlogEntry, Trip, TripComment, NewsFeedEntry, TripPhoto
from django.contrib.auth.models import User


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


COUNTRY_CHOICES = [(country.name, country.name) for country in countries] # From pycountry

class BlogEntryCreateForm(forms.ModelForm):
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
        fields = ['title', 'body', 'city', 'country', 'active', 'trip']
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
                choices=COUNTRY_CHOICES,  
                attrs={
                    'class': 'form-control',
                },
            ),
            'active': forms.CheckboxInput({
                'class': 'form-control',
            }),
            'trip': forms.Select({
                'class': 'form-control',
            }),
        }

class ToggleBlogForm(forms.ModelForm):
    class Meta:
        model = BlogEntry
        fields = ['active']
        widgets = {
            'active': forms.HiddenInput(),
        }
    blog_id = forms.IntegerField(widget=forms.HiddenInput())

class TripCreateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'description', 'start_date', 'end_date', 'active']
        widgets = {
            'title': forms.TextInput({
                'class': 'form-control',
                'placeholder': 'Title',
            }),
            'description': forms.Textarea({
                'class': 'form-control',
                'placeholder': 'Description',
            }),
            'start_date': forms.DateInput({
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD',
            }),
            'end_date': forms.DateInput({
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD',
            }),
            'active': forms.CheckboxInput({
                'class': 'form-control',
            }),
        }
    
class TripUpdateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'description', 'start_date', 'end_date', 'active']
        widgets = {
            'title': forms.TextInput({
                'class': 'form-control',
                'placeholder': 'Title',
            }),
            'description': forms.Textarea({
                'class': 'form-control',
                'placeholder': 'Description',
            }),
            'start_date': forms.DateInput({
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD',
            }),
            'end_date': forms.DateInput({
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD',
            }),
            'active': forms.CheckboxInput({
                'class': 'form-control',
            }),

        }

class TripCommentCreateForm(forms.ModelForm):
    class Meta:
        model = TripComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea({
                'class': 'form-control',
                'placeholder': 'Comment',
            }),
        }

class NewsFeedEntryCreateForm(forms.ModelForm):
    class Meta:
        model = NewsFeedEntry
        fields = ['title', 'body', 'active']
        widgets = {
            'title': forms.TextInput({
                'class': 'form-control',
                'placeholder': 'Title',
            }),
            'body': forms.Textarea({
                'class': 'form-control',
                'placeholder': 'Body',
            }),
            'active': forms.CheckboxInput({
                'class': 'form-control',
            }),
        }

class NewsFeedEntryUpdateForm(forms.ModelForm):
    class Meta:
        model = NewsFeedEntry
        fields = ['title', 'body', 'active']
        widgets = {
            'title': forms.TextInput({
                'class': 'form-control',
                'placeholder': 'Title',
            }),
            'body': forms.Textarea({
                'class': 'form-control',
                'placeholder': 'Body',
            }),
            'active': forms.CheckboxInput({
                'class': 'form-control',
            }),
        }

class TripPhotoCreateForm(forms.ModelForm):
    class Meta:
        model = TripPhoto
        fields = ['imageLink']
        widgets = {
            'imageLink': forms.TextInput({
                'class': 'form-control',
                'placeholder': 'Image Link',
            }),
        }
        
class UserCreationForm(forms.ModelForm):
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Repeat Password',
    }))

    terms_and_conditions = forms.BooleanField(label='I agree to the terms and conditions')
    subscribe_updates = forms.BooleanField(label='Subscribe for updates', required=False)

    class Meta:
        model = User
        fields = ['username','email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        if password != password_repeat:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    



