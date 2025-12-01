from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Movie model representing the movies table
class Movie(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(150))
    year = db.Column(db.Integer)
    genre = db.Column(db.String(100))

    def __repr__(self):
        return f"<Movie {self.title} ({self.year})>"

# Create the database and the tables for the model
with app.app_context():
    db.create_all()

@app.route('/', methods=[...])
def index():
    movies = Movie.query.all()  # Get all movies from the database
    return render_template('index.html', movies=movies)

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        #get items from form
        title = request.form.get('title', '').strip()
        director = request.form.get('director', '').strip()
        year = request.form.get('year', '').strip()
        genre = request.form.get('genre', '').strip()

        try:
            year_val = int(year) if year else None
        except ValueError:
            return redirect(url_for('add_movie'))


        # Create a new movie entry
        new_movie = Movie(
            title=title,
            director=director or None,
            year=year_val,
            genre=genre or None,)

        # Add to the session and commit to the database
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_movie.html')

if __name__ == '__main__':
    app.run(debug=True)
