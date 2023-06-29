import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "root",
    "password": "RangerUp1515!",
    "host": "localhost",
    "database": "movies",
    "raise_on_warnings": True
}


def show_films(cursor, title):
    cursor.execute("""
        SELECT film_name, film_director, genre_name, studio_name, film_runtime 
        FROM film 
        INNER JOIN genre ON film.genre_id=genre.genre_id 
        INNER JOIN studio ON film.studio_id=studio.studio_id
    """)

    films = cursor.fetchall()

    print("\n -- {} --".format(title))

    for film in films:
        print("\n Film Name: {}\n Director: {}\n Genre Name ID: {}\n Studio Name: {}\n".format(
            film[0], film[1], film[2], film[3]))


db = None

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    # Call the show_films method
    show_films(cursor, 'DISPLAYING FILMS')

    ## Inserting a new film into film table, use existing genre_id and studio_id
    cursor.execute("""
        INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
        VALUES ('The Matrix', '1999', 136, 'The Wachowski Brothers', 3, 2)
    """)
    db.commit()

    # Call the show_films method
    show_films(cursor, 'DISPLAYING FILMS AFTER INSERT')

    ## update the alien film to a genre of horor
    cursor.execute("""
        UPDATE film SET genre_id=1 WHERE film_name='Alien'
    """)
    db.commit()

    # Call the show_films method
    show_films(cursor, 'DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror')

    ## delete the gladitor film
    cursor.execute("""
        DELETE FROM film WHERE film_name='Gladiator'
    """)
    db.commit()

    # Call the show_films method
    show_films(cursor, 'DISPLAYING FILMS AFTER DELETE- Deleted Gladiator')

    input("\n\n Press any key to continue...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("\n Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("\n Database does not exist")
    else:
        print(err)
finally:
    if db:
        db.close()
