from flask import Blueprint, jsonify, request
from flask_login import login_required

from . import db
from .models import Movie

api = Blueprint('api', __name__)

@api.route('/api/movies', methods=['GET'])
@login_required
def get_movies():
    movies = Movie.query.all()
    data = [
        {
            "id": m.id,
            "title": m.title,
            "director": m.director,
            "year": m.year,
            "genre": m.genre
        }
        for m in movies
    ]
    return jsonify(data)

@api.route('/api/movie/<int:movie_id>', methods=['GET'])
@login_required
def get_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return jsonify({
        "id": movie.id,
        "title": movie.title,
        "director": movie.director,
        "year": movie.year,
        "genre": movie.genre
    })

@api.route('/api/movies' , methods=['POST'])
@login_required
def add_movie():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Missing "title"'}), 400

    new_movie = Movie(
        title=data['title'],
        director=data['director'],
        year=data['year'],
        genre=data['genre'],
    )
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({"id": new_movie.id, "title": new_movie.title, "director": new_movie.director,
                    "year": new_movie.year, "genre": new_movie.genre }), 201

@api.route('/api/movies/<int:movie_id>', methods=['DELETE'])
@login_required
def delete_movie_api(movie_id):
    # Fetch the movie by ID
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    # Delete the movie
    db.session.delete(movie)
    db.session.commit()

    return jsonify({"message": f"Movie with id {movie_id} deleted successfully"}), 200
