from flask import Blueprint, jsonify, request
from flask_login import login_required

from database_drive_webtech.flask_application_assignment import db
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
        director=data.get['director'],
        year=data.get['year'],
        genre=data.get['genre'],
    )
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({})

