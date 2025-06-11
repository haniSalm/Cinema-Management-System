from typing import Any
from django.core.management.base import BaseCommand, CommandError
from users.models import *
import requests, json, wget, os
from bliss_cinema.settings import STATIC_DIR
import shutil
POPULAR = 1
NOWPLAYING = 2
# -----functions----- 
def create_directory(directory_path):
    try:
        os.mkdir(directory_path)
    except OSError as e:
        raise CommandError(f"Error occurred while creating directory '{directory_path}': {e}")

def delete_directory(directory_path):
    try:
        shutil.rmtree(directory_path)
    except OSError as e:
        raise CommandError(f"Error occurred while deleting directory '{directory_path}': {e}")

def download_image(url, save_as, image_name):
    curr_name = wget.download(url, save_as)
    full_curr_path = os.path.join(save_as, curr_name)
    full_final_path = os.path.join(save_as, image_name)
    os.rename(full_curr_path, full_final_path)

def get_movies(movies_dictionaries, movies_url):
    create_directory(os.path.join(STATIC_DIR, 'posters'))
    # -variables-
    config_url = "https://api.themoviedb.org/3/configuration"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlMDVhMjUwZWJhZWE2MTE1NmRhY2ZkZjRmM2FmNDUxMSIsInN1YiI6IjY2MzFmNGI2ZmU2YzE4MDEyYzJlZTdjOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.jXAgFvsG4clB3DoRpJBaTx47BH02XHGdjYfsIjVy4kU"
    }
    # -getting list of movies-
    response = requests.get(movies_url, headers=headers)
    movies_list = json.loads(response.text)
    # -getting poster_size and base_url for downloading images-
    response = requests.get(config_url, headers=headers)
    config = json.loads(response.text)
    poster_size = config['images']['poster_sizes'][-1]
    base_url = config['images']['base_url']
    # -iterating over list of movies-
    for movie in movies_list["results"]:
        # -making dictionary args-
        original_title = movie['original_title']
        year = movie['release_date']
        save_in = None
        image_name = None
        # -downloading poster-
        poster_path = movie['poster_path']
        if poster_path is not None:
            image_name = f"{movie['original_title']}.jpg"
            image_url = base_url + '/' + poster_size + '/' + poster_path
            save_in = os.path.join(STATIC_DIR, "posters")
            download_image(image_url, save_in, image_name)
        movies_dictionaries.append({
            "original_title": original_title,
            "released": year,
            "dirpath": save_in,
            "image_name": image_name
        })

def get_popular_movies(movies_dictionaries):
    lang = "en-US"
    pages = 1
    region = "PK"
    movies_url = f"https://api.themoviedb.org/3/movie/popular?language={lang}&page={pages}&region={region}"
    get_movies(movies_dictionaries, movies_url)

def get_nowplaying_movies(movies_dictionaries):
    lang = "en-US"
    pages = 1
    region = "PK"
    movies_url = f"https://api.themoviedb.org/3/movie/now_playing?language={lang}&page={pages}&region={region}"
    get_movies(movies_dictionaries, movies_url)

def add_movies_to_database(category):
    movies = []
    if (category == POPULAR):
        get_popular_movies(movies)
    elif (category == NOWPLAYING):
        get_nowplaying_movies(movies)
    else:
        raise CommandError('invalid call by handle method to add_movies_to_database function')
    
    for movie in movies:
        m_obj = Movie.objects.create(
            original_title=movie['original_title'],
            released=movie['released'],
        )
        if movie['image_name'] is not None:
            m_obj.poster.save(
                movie['image_name'], 
                open(os.path.join(movie['dirpath'], movie['image_name']), 'rb'), 
                save=True
            )
        if (category == POPULAR):
            tm_obj = TopMovie.objects.create(movie=m_obj)
            tm_obj.save()
        else:
            np_obj = NowPlaying.objects.create(movie=m_obj)
            np_obj.save()
    delete_directory(os.path.join(STATIC_DIR, "posters"))

class Command(BaseCommand):
    help = 'gets movies data from the web'
    def handle(self, *args: Any, **options: Any):
        add_movies_to_database(POPULAR)
        add_movies_to_database(NOWPLAYING)