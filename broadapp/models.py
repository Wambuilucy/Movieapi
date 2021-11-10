from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.profile.user.id, filename)
  

# class MyModel(models.Model):
#     year = models.IntegerField(_('year'), validators=[MinValueValidator(1984), max_value_current_year])

# def year_choices():
#     return [(r,r) for r in range(1984, datetime.date.today().year+1)]

CATEGORIES= (
    ('documentary','DOCUMENTARY'),
    ('martial arts','MARTIAL ARTS'),
    ('historical','HISTORICAL'),
    ('adventure','ADVENTURE'),
    ('animation','ANIMATION'),
    ('thriller','THRILLER'),
    ('romance','ROMANCE'),
    ('fantasy','FANTASY'),
    ('horror','HORROR'),
    ('action','ACTION'),
    ('comedy','COMEDY'),
    ('sci-fi','SCI-FI'),
    ('drama','DRAMA'),
)


STATUS = (
    ('recently added','RECENTLY ADDED'),
    ('most watched','MOST WATCHED'),
    ('top rated','TOP RATED'),
    ('trending','TRENDING'),
    ('popular','POPULAR'),
    ('upcoming','UPCOMING'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatar/', default= 'avatar/deafult.png')

class Episode(models.Model):
    episodes_1 = models.FileField(upload_to='series/', blank=True, null=True)
    episodes_2 = models.FileField(upload_to='series/', blank=True, null=True)
    episodes_3 = models.FileField(upload_to='series/', blank=True, null=True)
    episodes_4 = models.FileField(upload_to='series/', blank=True, null=True)
    episodes_5 = models.FileField(upload_to='series/', blank=True, null=True)
    episodes_6 = models.FileField(upload_to='series/', blank=True, null=True)
    episodes_7 = models.FileField(upload_to='series/', blank=True, null=True)
    episodes_8 = models.FileField(upload_to='series/', blank=True, null=True)
    episodes_9 = models.FileField(upload_to='series/', blank=True, null=True)
    episodes_10 = models.FileField(upload_to='series/', blank=True, null=True)
    episodes_11 = models.FileField(upload_to='series/', blank=True, null=True)
    episodes_12 = models.FileField(upload_to='series/', blank=True, null=True)
    episodes_13 = models.FileField(upload_to='series/', blank=True, null=True)
    
class Show(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True) 
    episodes = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='tv_episodes')      
    title = models.CharField(max_length=120)
    poster = models.ImageField(upload_to='images/')
    category = models.CharField(choices=CATEGORIES, max_length=15)
    status = models.CharField(choices=STATUS, max_length=21)
    release_year = models.IntegerField()
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.title
    

class Movie(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)    
    title = models.CharField(max_length=120)
    video = models.FileField(upload_to='videos/')
    poster = models.ImageField(upload_to='images/')
    category = models.CharField(choices=CATEGORIES, max_length=15)
    status = models.CharField(choices=STATUS, max_length=21)
    release_year = models.IntegerField()
    description = models.TextField(max_length=1000)
    
    def __str__(self):
        return self.title
    

# forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    