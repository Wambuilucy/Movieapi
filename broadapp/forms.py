from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ClearableFileInput, DateField
from django.forms.widgets import NumberInput
from dobwidget import DateOfBirthWidget
from .models import *
from datetime import datetime

# from django.core.files.images import get_image_dimensions

# def possible_years(first_year_in_scroll, last_year_in_scroll):
#     p_year = []
#     for i in range(first_year_in_scroll, last_year_in_scroll, -1):
#         p_year_tuple = str(i), i
#         p_year.append(p_year_tuple)
#     return p_year

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2') 
        
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        # release_year = forms.ChoiceField(choices=possible_years(((datetime.now()).year), 1900),label='Release Year',)
        fields = ('title', 'video', 'poster','category','status','release_year', 'description')
        # widgets = {
        #     'release_year': DateOfBirthWidget(),
        # }
        
class SeriesForm(forms.ModelForm):
    class Meta:
        model = Show
        exclude = ['uuid', 'episodes']
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'color'}),
        }
        
class EpisodesForm(forms.ModelForm):
    class Meta:
        model = Episode
        # file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
        fields = '__all__'
        # widgets = {
        #     'episodes': ClearableFileInput(attrs={'multiple': True}),
        # }
        