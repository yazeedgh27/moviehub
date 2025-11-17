from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "movies.db")

# ============================
# DATABASE
# ============================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def insert_contact(name, email, message):
    print("🔥 INSERT CONTACT CALLED!")   # DEBUG
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
                (name, email, message))
    conn.commit()
    conn.close()


# ============================
# MOVIES DATA
# ============================
MOVIES = [
    {
        "id": 1,
        "title": "Inception",
        "rating": 8.8,
        "year": 2010,
        "poster": "https://m.media-amazon.com/images/I/51zUbui+gbL._AC_.jpg",
        "genre": "Action, Sci-Fi",
        "description": "A thief enters dreams to erase his past."
    },
    {
        "id": 2,
        "title": "Interstellar",
        "rating": 8.6,
        "year": 2014,
        "poster": "https://image.tmdb.org/t/p/w500/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg",
        "genre": "Adventure, Drama, Sci-Fi",
        "description": "Explorers travel through a wormhole."
    },
    {
        "id": 3,
        "title": "The Dark Knight",
        "rating": 9.0,
        "year": 2008,
        "poster": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "genre": "Action, Crime, Drama",
        "description": "Batman faces the Joker."
    },
    {
        "id": 4,
        "title": "The Matrix",
        "rating": 8.7,
        "year": 1999,
        "poster": "https://m.media-amazon.com/images/I/51EG732BV3L._AC_.jpg",
        "genre": "Action, Sci-Fi",
        "description": "A hacker discovers the truth about reality."
    },
    {
        "id": 5,
        "title": "Avatar",
        "rating": 7.8,
        "year": 2009,
        "poster": "https://image.tmdb.org/t/p/w500/jRXYjXNq0Cs2TcJjLkki24MLp7u.jpg",
        "genre": "Sci-Fi, Adventure",
        "description": "A soldier integrates into an alien tribe."
    },
    {
        "id": 6,
        "title": "Gladiator",
        "rating": 8.5,
        "year": 2000,
        "poster": "https://image.tmdb.org/t/p/w500/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg",
        "genre": "Action, Drama",
        "description": "A Roman general seeks revenge."
    },
    {
        "id": 7,
        "title": "The Shawshank Redemption",
        "rating": 9.3,
        "year": 1994,
        "poster": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
        "genre": "Drama",
        "description": "Two imprisoned men bond over hope."
    },
    {
        "id": 8,
        "title": "Fight Club",
        "rating": 8.8,
        "year": 1999,
        "poster": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
        "genre": "Drama",
        "description": "An underground fighting club emerges."
    },
    {
        "id": 9,
        "title": "Forrest Gump",
        "rating": 8.8,
        "year": 1994,
        "poster": "https://image.tmdb.org/t/p/w500/saHP97rTPS5eLmrLQEcANmKrsFl.jpg",
        "genre": "Drama, Romance",
        "description": "The story of Forrest Gump."
    },
    {
        "id": 10,
        "title": "Avengers: Endgame",
        "rating": 8.4,
        "year": 2019,
        "poster": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
        "genre": "Action, Adventure",
        "description": "Heroes unite to restore balance."
    },
    {
        "id": 11,
        "title": "Joker",
        "rating": 8.4,
        "year": 2019,
        "poster": "https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",
        "genre": "Crime, Drama",
        "description": "The origin story of Joker."
    },
    {
        "id": 12,
        "title": "Titanic",
        "rating": 7.8,
        "year": 1997,
        "poster": "https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",
        "genre": "Drama, Romance",
        "description": "A love story aboard the Titanic."
    },
    {
        "id": 13,
        "title": "The Godfather",
        "rating": 9.2,
        "year": 1972,
        "poster": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
        "genre": "Crime, Drama",
        "description": "The mafia family's dark saga."
    },
    {
        "id": 14,
        "title": "The Lion King",
        "rating": 8.5,
        "year": 1994,
        "poster": "https://image.tmdb.org/t/p/w500/sKCr78MXSLixwmZ8DyJLrpMsd15.jpg",
        "genre": "Animation, Adventure, Drama",
        "description": "A young lion prince flees his kingdom to learn bravery."
    },
    {
        "id": 15,
        "title": "Dune",
        "rating": 8.0,
        "year": 2021,
        "poster": "https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg",
        "genre": "Sci-Fi, Adventure",
        "description": "A battle for control of a desert planet."
    }
]


# ============================
# ROUTES
# ============================

@app.route('/')
def home():
    sorted_movies = sorted(MOVIES, key=lambda m: m["rating"], reverse=True)
    featured = sorted_movies[:6]
    return render_template("index.html", movies=featured)


@app.route('/movies')
def movies():
    return render_template("movies.html", movies=MOVIES)


@app.route('/movie/<int:id>')
def movie_details(id):
    movie = next((m for m in MOVIES if m["id"] == id), None)
    return render_template("movie_details.html", movie=movie)


@app.route('/movies-by-genre')
def movies_by_genre():
    genres = {}

    for movie in MOVIES:
        genre_list = movie["genre"].split(",")
        for g in genre_list:
            g = g.strip()
            if g not in genres:
                genres[g] = []
            genres[g].append(movie)

    return render_template("movies_by_genre.html", genres=genres)


@app.route('/about')
def about():
    return render_template("about.html")


# ⭐⭐ CONTACT FIXED ⭐⭐
@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        insert_contact(name, email, message)
        return render_template("thanks.html", name=name)

    return render_template("contact.html")


# ============================
# STARTUP
# ============================
with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)






