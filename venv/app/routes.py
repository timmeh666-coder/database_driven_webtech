from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from .models import Movie, User

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

@main.route('/', methods=['GET'])
@login_required
def index():
    movies = Movie.query.all()  # Get all movies from the database
    return render_template('index.html', movies=movies)

@main.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        # get items from form
        title = request.form.get('title', '').strip()
        director = request.form.get('director', '').strip()
        year = request.form.get('year', '').strip()
        genre = request.form.get('genre', '').strip()

        try:
            year_val = int(year) if year else None
        except ValueError:
            return redirect(url_for('main.add_movie'))

        # Create a new movie entry
        new_movie = Movie(
            title=title,
            director=director or None,
            year=year_val,
            genre=genre or None,
        )

        # Add to the session and commit to the database
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('add_movie.html')

@main.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    movie = Movie.query.get(movie_id)

    if request.method == 'POST':
        # get items from form
        title = request.form.get('title', '').strip()
        director = request.form.get('director', '').strip()
        year = request.form.get('year', '').strip()
        genre = request.form.get('genre', '').strip()

        try:
            year_val = int(year) if year else None
        except ValueError:
            return redirect(url_for('main.edit_movie', movie_id=movie_id))

        # Create a new movie entry
        movie.title = title
        movie.director = director or None
        movie.year = year_val
        movie.genre = genre or None

        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('add_movie.html', movie=movie)

@main.route('/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful!", "success")
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
