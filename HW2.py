from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route('/')
def main_page():
    conn = sqlite3.connect('hw2.db')
    cur = conn.cursor()
    res = cur.execute('SELECT id, poster, name FROM film order by added_at DESC limit 10')
    result = res.fetchall()
    return result

@app.route('/register', methods=['POST'])
def user_register():
    return 'register'

@app.post('/login')
def user_login():
    return 'login'

@app.route('/logout', methods=['GET'] )
def user_logout():
    return 'logout'

@app.route('/user/<user_id>', methods=['GET', 'PATCH'])
def user_profile(user_id):
    return f'User {user_id}'


@app.route('/user/<user_id>', methods=['DELETE'])
def user_delete(user_id):
    return f'User {user_id} deleted'

@app.route('/films', methods=['GET']) #  записать все фильмы
def films():
    conn = sqlite3.connect('hw2.db')
    cur = conn.cursor()
    res = cur.execute('SELECT id, poster, name FROM film order by added_at DESC')
    result = res.fetchall()
    return result

@app.route('/films', methods=['POST'])
def film_add():
    return 'films added'

@app.route('/films/<film_id>', methods=['GET'])
def film_info(film_id):
    conn = sqlite3.connect('hw2.db')
    cur = conn.cursor()
    res = cur.execute(f'SELECT * FROM film WHERE id={film_id}')
    result = res.fetchone()

    actors = cur.execute(f'SELECT * FROM actor join actor_film on actor.id == actor_film.actor_id where film_id={film_id}').fetchall()
    genres = cur.execute(f'SELECT * FROM genre_film where film_id={film_id}').fetchall()

    return f'Film {film_id} is {result}, actors {actors}, genres {genres}'

@app.route('/films/<film_id>', methods=['PUT'])
def film_update(film_id):
    return f'film {film_id} updated'

@app.route('/films/<film_id>', methods=['DELETE'])
def film_delete(film_id):
    return f'film {film_id} deleted'

@app.route('/films/<film_id>/rating', methods=['GET'])# Домашнее задание добавить отзывы о фильмах
def film_rating_info(film_id):
    conn = sqlite3.connect('hw2.db')
    cur = conn.cursor()
    res = cur.execute(f'SELECT description FROM film')
    result = res.fetchall()
    return f'film {film_id} rating is {result}'

@app.route('/films/<film_id>/rating', methods=['POST'])
def film_rating(film_id):
    return f'Film {film_id} rated'

@app.route('/films/<film_id>/rating/<feedback_id>', methods=['DELETE'])
def film_rating_delete(film_id, feedback_id):
    return f'film {film_id} rating {feedback_id} deleted'

@app.route('/films/<film_id>/rating/<feedback_id>', methods=['PUT'])
def film_rating_update(film_id, feedback_id):
    return f'film {film_id} rating {feedback_id} updated'

@app.route('/user/<user_id>/lists', methods=['GET', 'POST'])
def user_list_add(user_id):
    return f'user {user_id} list added'

@app.route('/user/<user_id>/lists/<list_id>', methods=['DELETE'])
def user_list_delete(user_id):
    return f'user {user_id} list deleted'

@app.route('/user/<user_id>/lists/<list_id>', methods=['GET', 'POST'])
def user_list_item(user_id, list_id):
    return f'user {user_id} list item {list_id}'

@app.route('/user/<user_id>/lists/<list_id>/<film_id>', methods=['DELETE'])
def user_list_item_delete(user_id, list_id, film_id):
    return f'user {user_id} list item {list_id} deleted'



if __name__ == '__main__':
    app.run()