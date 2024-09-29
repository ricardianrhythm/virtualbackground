import os
import requests

def get_book_cover(book_name):
    # Get Google Books API key from environment variable (optional)
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')

    base_url = f"https://www.googleapis.com/books/v1/volumes?q={book_name}"
    
    if api_key:
        base_url += f"&key={api_key}"
    
    response = requests.get(base_url)
    data = response.json()

    if 'items' in data:
        book_cover = data['items'][0]['volumeInfo'].get('imageLinks', {}).get('thumbnail')
        return book_cover
    return None