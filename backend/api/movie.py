import os
import requests

def get_movie_poster(movie_name):
    # Get TMDB API key from environment variable
    api_key = os.getenv('TMDB_API_KEY')
    
    if not api_key:
        raise Exception("TMDB API key is missing")
    
    base_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
    response = requests.get(base_url)
    data = response.json()

    if data['results']:
        poster_path = data['results'][0]['poster_path']
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None