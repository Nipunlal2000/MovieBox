from django import forms
from .models import *


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genres
        fields = ['name']


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'description', 'release_year', 'actors', 'genres', 'trailer_link']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'email']
