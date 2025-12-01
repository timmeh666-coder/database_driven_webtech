import requests
from fastjsonschema.ref_resolver import get_id

# Base URL of your running Flask app
BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()
# --- 1. Login ---
login_data = {
    "username": "Tim",
    "password": "1"
}

login_response = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=True)

if login_response.url.endswith("/login"):
    print("Login failed")
else:
    print("Login successful!")
    movies_response = session.get(f"{BASE_URL}/api/movies")
    if movies_response.status_code == 200:
        movies = movies_response.json()

        print("Movies:", movies)
    else:
        print("Failed to get movies:", movies_response.text)

# --- 3. Add a new movie ---
new_movie = {
    "title": "The Matrix",
    "director": "Wachowski",
    "year": 1999,
    "genre": "Sci-Fi"
}

add_response = session.post(f"{BASE_URL}/api/movies", json=new_movie)


if add_response.status_code == 201:
    print("Movie added successfully!")
    movie_id = add_response.json().get("id")
else:
    print("Failed to add movie:", add_response.text)

if movies_response.status_code == 200:
        movies = movies_response.json()

        print("Movies:", movies)
else:
        print("Failed to get movies:", movies_response.text)

if movie_id:
    delete_response = session.delete(f"{BASE_URL}/api/movies/{movie_id}")
    if delete_response.status_code == 200:
        print(f"Movie with ID {movie_id} deleted successfully!")
    else:
        print("Failed to delete movie:", delete_response.text)
else:
    print("Failed to delete movie: no movie id")

if movies_response.status_code == 200:
        movies = movies_response.json()

        print("Movies:", movies)
else:
        print("Failed to get movies:", movies_response.text)