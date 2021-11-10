# from typing_extensions import Required
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from .models import *
from django.core.paginator import Paginator,PageNotAnInteger, InvalidPage
from .forms import *
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
from isodate import parse_duration
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import os
import requests

def index(request):
    
    return render(request, 'index.html')

def play_movies(request):

    return render(request, 'content.html')

def series(request):
    return render(request, 'content_series.html')

def movies_series(request):
    return render(request, 'content_movies_series.html')

def all_movies(request):
    object_random = Movie.objects.order_by('?')
    object_list = Movie.objects.all()
    paginator = Paginator(object_list,4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'movies/movies.html', {'object_list':object_list,'page_obj': page_obj, 'object_random' : object_random})
    
def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, uuid=movie_id)
    return render(request, 'movies/movie_details.html', {'movie':movie})

def all_series(request):
    object_list = Show.objects.all()
    # paginator = Paginator(object_list,18)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    return render(request, 'series/series.html', {'object_list':object_list})

def series_details(request, id):
    series = get_object_or_404(Show, uuid=id)
    return render(request, 'series/series_details.html', {'series':series})

def series_details_episode(request, id, slug):
    series = get_object_or_404(Show, uuid=id)
    shows = get_object_or_404(Show, episodes=slug)
    return HttpResponseRedirect(reverse('Series_Details_Episode'))
    
def movie_trailers(request):
    object_list = Movie.objects.all()
    object_list_2 = Show.objects.all()
    paginator = Paginator(object_list,16)
    paginator_2 = Paginator(object_list_2,16)
    
    page_number = request.GET.get('page')
    # page_number_2 = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_obj_2 = paginator_2.get_page(page_number)
    return render(request, 'trailers/movie_trailers.html', {'object_list':object_list,'page_obj': page_obj, 'object_list_2':object_list_2,'page_obj_2': page_obj_2}) 

def trailers(request):
    videos = []
    
    # if request.method == 'POST':
        
    #     search_url = 'https://www.googleapis.com/youtube/v3/search'
    #     video_url = 'https://www.googleapis.com/youtube/v3/videos'
                
    #     search_params = {
    #         'part' : 'snippet',
    #         'q' : request.POST['search'],
    #         'key' : settings.YOUTUBE_DATA_API_KEY,
    #         'maxResults' : 6,
    #         'type' : 'video'
    #     }
    #     video_ids = []
    #     r = requests.get(search_url, params=search_params)
    #     results = r.json()['items']
        
    #     for result in results:
    #         video_ids.append(result['id']['videoId'])
            
    #     video_params = {
    #         'key' : settings.YOUTUBE_DATA_API_KEY,
    #         'part' : 'snippet, contentDetails, statistics',
    #         'id' : ','.join(video_ids),
    #         'maxResults' : 6,
    #     }
        
    #     r = requests.get(video_url, video_params)
        
    #     results = r.json()['items']
        
        
    #     for result in results:
    #         print(result)
    #         # print(result['snippet']['title'])
    #         # print(result['snippet']['description'])
    #         # print(result['statistics']['viewCount'])
    #         # print(result['statistics']['likeCount'])
    #         # print(result['id'])
    #         # print(parse_duration(result['contentDetails']['duration']).total_seconds()//60)
    #         # print(result['snippet']['thumbnails']['high']['url'])
            
    #         video_data = {
    #             'id' : result['id'],
    #             'title' : result['snippet']['title'],
    #             'poster' : result['snippet']['thumbnails']['high']['url'],
    #             'url' : f'https://www.youtube.com/watch?v={result["id"]}',
    #             'description' : result['snippet']['description'],
    #             'views' : result['statistics']['viewCount'],
    #             'likes' : result['statistics']['likeCount'],
    #             'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
    #         }
            
    #         videos.append(video_data)
            
        
    content = {
        'videos' : 'videos',
    }
    
    return render(request, 'trailers/trailers.html', content)

def upload(request):
    return render(request, 'upload.html')

@csrf_exempt
def upload_series(request):
    
    if request.method == "POST":
        
        form = SeriesForm(request.POST, request.FILES)
        form_E = EpisodesForm(request.POST, request.FILES)
        
        if form.is_valid() and form_E.is_valid():
            data_E = form_E.save()
            data_E.save()
            data = form.save(commit=False)
            data.episodes = data_E
            data.save()
            return JsonResponse({'data':'TV Show uploaded'})
        
        else:
            # form = SeriesForm()
            # form_E = SeriesForm()
            return JsonResponse({'data':'Something went wrong!!'})
    
    return render(request, 'movies/upload_series.html', {'form_E':SeriesForm, 'form':EpisodesForm})

@csrf_exempt
def upload_movie(request):
    
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()
            data.save()
            return JsonResponse({'data':'Movie uploaded'})
        else:
            return JsonResponse({'data':'Something went wrong!!'})
        
    return render(request, 'movies/upload_movie.html', {'form':MovieForm})
        
def test(request,title):
    trailer = get_object_or_404(Movie, title=title)
    videos = []
    # if request.method == 'POST':
        
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
            
    search_params = {
        'part' : 'snippet',
        'q' : trailer.title + ' trailer',
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'maxResults' : 2,
        'type' : 'video'
    }
    video_ids = []
    r = requests.get(search_url, params=search_params)
    results = r.json()['items']
    
    for result in results:
        video_ids.append(result['id']['videoId'])
              
    video_params = {
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'part' : 'snippet, contentDetails, statistics',
        'id' : ','.join(video_ids),
        'maxResults' : 2,
    }
    
    r = requests.get(video_url, video_params)
    
    results = r.json()['items']
    
    
    for result in results:
        
        try:   
        
            video_data = {
                        
                'id' : result['id'],
                'title' : result['snippet']['title'],
                'poster' : result['snippet']['thumbnails']['high']['url'],
                'url' : f'https://www.youtube.com/watch?v={result["id"]}',
                'description' : result['snippet']['description'],
                'views' : result['statistics']['viewCount'],
                'likes' : result['statistics']['likeCount'],
                # 'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                'duration' : parse_duration(result['contentDetails']['duration']),            
            }
            
        except Exception: 
            
            video_data = {      
                        
                'id' : result['id'],
                'title' : result['snippet']['title'],
                'poster' : result['snippet']['thumbnails']['high']['url'],
                'url' : f'https://www.youtube.com/watch?v={result["id"]}',
                'description' : result['snippet']['description'],
                'views' : result['statistics']['viewCount'],
                'likes' : 'NA',
                # 'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                'duration' : 'N/A',            
            }
        
        # print(video_data)
        
        videos.append(video_data)
        
    content = {
        'videos' : videos,
        'trailer':trailer
    }
        
    return render(request, 'trailers/test.html', content)




def test_series(request,title):
    trailer = get_object_or_404(Show, title=title)
    videos = []
    # if request.method == 'POST':
        
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
            
    search_params = {
        'part' : 'snippet',
        'q' : trailer.title + ' trailer',
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'maxResults' : 2,
        'type' : 'video'
    }
    video_ids = []
    r = requests.get(search_url, params=search_params)
    results = r.json()['items']
    
    for result in results:
        video_ids.append(result['id']['videoId'])
              
    video_params = {
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'part' : 'snippet, contentDetails, statistics',
        'id' : ','.join(video_ids),
        'maxResults' : 2,
    }
    
    r = requests.get(video_url, video_params)
    
    results = r.json()['items']
    
    
    for result in results:
        
        try:   
        
            video_data = {
                        
                'id' : result['id'],
                'title' : result['snippet']['title'],
                'poster' : result['snippet']['thumbnails']['high']['url'],
                'url' : f'https://www.youtube.com/watch?v={result["id"]}',
                'description' : result['snippet']['description'],
                'views' : result['statistics']['viewCount'],
                'likes' : result['statistics']['likeCount'],
                # 'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                'duration' : parse_duration(result['contentDetails']['duration']),            
            }
            
        except Exception: 
            
            video_data = {      
                        
                'id' : result['id'],
                'title' : result['snippet']['title'],
                'poster' : result['snippet']['thumbnails']['high']['url'],
                'url' : f'https://www.youtube.com/watch?v={result["id"]}',
                'description' : result['snippet']['description'],
                'views' : result['statistics']['viewCount'],
                'likes' : 'NA',
                # 'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds()//60),
                'duration' : 'N/A',            
            }
        
        # print(video_data)
        
        videos.append(video_data)
        
    content = {
        'videos' : videos,
        'trailer':trailer
    }
        
    return render(request, 'trailers/test_series.html', content)




 


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})

@login_required
def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('/')

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)