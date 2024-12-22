import sqlite3

def connect_db():
    return sqlite3.connect("C:\et,g\kodproject\OwnProject\movie.db")

def get_random_movie():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, vote_average FROM movies ORDER BY RANDOM() LIMIT 1")
    movie = cursor.fetchone()
    conn.close()
    return movie

def get_genres():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT genre FROM genres")
    genres = [row[0] for row in cursor.fetchall()]
    conn.close()
    return genres

def get_movies_by_genre(genre):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT movies.id, movies.title, movies.vote_average
        FROM movies
        JOIN movies_genres ON movies.id = movies_genres.movie_id
        JOIN genres ON movies_genres.genre_id = genres.genre_id
        WHERE genres.genre = ?
        """,
        (genre,)
    )
    movies = cursor.fetchall()
    conn.close()
    return movies
