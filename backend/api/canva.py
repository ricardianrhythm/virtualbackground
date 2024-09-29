from PIL import Image
import requests
from io import BytesIO

def create_final_image(movie_poster_url, book_cover_url, user_photo):
    # Open the movie poster and book cover from URLs
    movie_poster = Image.open(BytesIO(requests.get(movie_poster_url).content))
    book_cover = Image.open(BytesIO(requests.get(book_cover_url).content))

    # Open the user's uploaded photo
    user_image = Image.open(user_photo.stream)

    # Create a new blank image (final canvas) and paste the images onto it
    final_image = Image.new("RGB", (1500, 900))  # Adjust size as needed

    final_image.paste(movie_poster, (0, 0))  # Top-left corner
    final_image.paste(book_cover, (500, 0))  # Adjust positioning
    final_image.paste(user_image, (1000, 0))  # Adjust positioning

    # Save the final image and return the path
    final_image_path = "/path/to/save/final_image.jpg"
    final_image.save(final_image_path)
    
    return final_image_path