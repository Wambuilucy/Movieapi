from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('', views.index, name='MainPage'),
    path('upload', views.upload, name='Upload'),
    path('play_movies', views.play_movies, name='PlayMovies'),
    path('stream_content', views.series, name='Stream'),
    path('movies_&_series', views.movies_series, name='MoviesSeries'),
    path('all_movies', views.all_movies, name='All_Movies'),
    path('<uuid:movie_id>', views.movie_details, name='Movie_Details'),
    path('upload-series', views.upload_series, name='Upload_Series'),
    path('upload-movie', views.upload_movie, name='Upload_Movie'),
    path('all_series', views.all_series, name='All_Series'),
    path('single_series/<uuid:id>', views.series_details, name='Series_Details'),
    path('single_series/<uuid:id>/<slug:slug>', views.series_details_episode, name='Series_Details_Episode'),
    path('movie_trailers', views.movie_trailers, name='Movie_Trailers'),
    path('movie_trailers/404', views.trailers, name='Trailer'),
    path('movie_trailers/trailer/<title>', views.test, name='Test'),
    path('movie_trailers/series_trailer/<title>', views.test_series, name='Test_Series'),
    # path('accounts/', include('django_registration.backends.one_step.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path("register", views.signup, name="Register"),
    path("logout", views.logout, name= "Logout"),
    path('login', views.login_request, name='Login'),
    ]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns+= static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)