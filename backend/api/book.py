import requests

def get_book_cover(book_name):
    base_url = f"https://www.googleapis.com/books/v1/volumes?q={book_name}"
    response = requests.get(base_url)
    data = response.json()

    if 'items' in data:
        book_cover = data['items'][0]['volumeInfo'].get('imageLinks', {}).get('thumbnail')
        return book_cover
    return None