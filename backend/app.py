from flask import Flask, request, jsonify
from api.movie import get_movie_poster
from api.book import get_book_cover
from api.upload import validate_image
from api.canva import create_final_image
from database import initialize_firestore, save_user_data

app = Flask(__name__)

# Initialize Firestore
db = initialize_firestore()

@app.route('/api/process', methods=['POST'])
def process_form():
    movie = request.form['movie']
    book = request.form['book']
    file = request.files['file']

    # Get movie poster and book cover
    movie_poster = get_movie_poster(movie)
    book_cover = get_book_cover(book)

    # Validate and process the uploaded image
    if not validate_image(file):
        return jsonify({'error': 'Invalid image dimensions'}), 400

    # Create final image using Canva API or PIL
    final_image_url = create_final_image(movie_poster, book_cover, file)

    # Save user data to Firestore
    doc_ref = save_user_data(db, movie, book, final_image_url)

    return jsonify({'final_image': final_image_url, 'doc_id': doc_ref.id})

if __name__ == '__main__':
    app.run(debug=True)