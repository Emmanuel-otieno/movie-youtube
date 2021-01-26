import requests
from isodate import parse_duration
from django.conf import Settings
from django.shortcuts import render

# Create your views here.
def index(request):
    search_url =' https://www.googleapis.com/youtube/v3/search'
    video_url ='https://www.googleapis.com/youtube/v3/videos' 
    search_params ={
        'part' : 'snippet',
        'q' : 'movies',
        'key' : 'AIzaSyA42cZYCxPcz0qWtM-7QNYsvoZD4yVCXmg',
        'maxResults' : 20,
        'type' : 'video'
    }
    video_ids = []

    r = requests.get(search_url, params=search_params)
    
    results =r.json()['items']
    videos = []
    for result in results:
        video_ids.append(result['id']['videoId'])

    video_params ={
        'key' : 'AIzaSyA42cZYCxPcz0qWtM-7QNYsvoZD4yVCXmg',
        'part' : 'snippet,contentDetails',
        'id' : ','.join(video_ids),
        'maxResults' : 20,
    }

    r = requests.get(video_url, params=video_params)

    results =r.json()['items']

    for result in results:

        video_data ={
            'title' :result['snippet']['title'],
            'id' : result['id'],
            'url':  f'https://www.youtube.com/watch?v={result["id"]}',
            'duration' : parse_duration(result['contentDetails']['duration']),
            'thumbnail' : result['snippet']['thumbnails']['high']['url']
        }
        videos.append(video_data)

    context ={
        'videos': videos
    }        

    return render(request, 'movies/index.html',context)