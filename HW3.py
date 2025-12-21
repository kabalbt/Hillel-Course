from flask import Flask
from flask import request
import sqlite3

app = Flask(__name__)

def film_dictionary(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class db_connection:
    def __init__(self):
        self.conn = sqlite3.connect('hw3.db')
        self.conn.row_factory = film_dictionary
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.close()

def get_db_result(query):
    conn = sqlite3.connect('hw3.db')
    conn.row_factory = film_dictionary
    cursor = conn.cursor()
    res = cursor.execute(query)
    result = res.fetchall()
    conn.close()
    return result



@app.route('/')
def main_page():
    with db_connection() as cur:
        result = cur.execute("SELECT id, poster, name FROM film order by added_at DESC limit 10").fetchall()

    #result = get_db_result('SELECT id, poster, name FROM film order by added_at DESC limit 10')
    return result

@app.route('/register', methods=['GET'])
def register_page():
    return """
    <form action="/register" method="POST">
    
  <label for="fname">First name:</label><br>
  <input type="text" id="fname" name="fname"><br>
  
  <label for="lname">Last name:</label><br>
  <input type="text" id="lname" name="lname"><br>
  
   <label for="password">password:</label><br>
  <input type="password" id="password" name="password"><br>
  
   <label for="login">login:</label><br>
  <input type="text" id="login" name="login"><br>
  
   <label for="email">email:</label><br>
  <input type="email" id="email" name="email"><br>
  
   <label for="birth_date">birth_date:</label><br>
  <input type="date" id="birth_date" name="birth_date"><br>
  
  
    <input type="submit" value="Submit">
    </form>
    """


@app.route('/register', methods=['POST'])
def user_register():
    first_name = request.form['fname']
    last_name = request.form['lname']
    password = request.form['password']
    login = request.form['login']
    email = request.form['email']
    birth_date = request.form['birth_date']

    with db_connection() as cur:
        cur.execute("INSERT INTO user (fname, lname, password, login, email, birth_dat) VALUES (?, ?, ?, ?, ?, ?)",
                    (first_name, last_name, password, login, email, birth_date))
    return 'Register'

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
    result = get_db_result('SELECT id, poster, name FROM film order by added_at DESC')
    return result

@app.route('/films', methods=['POST'])
def film_add():
    return 'films added'

@app.route('/films/<film_id>', methods=['GET'])
def film_info(film_id):
    with db_connection() as cur:
        result = cur.execute(f"SELECT * FROM film WHERE id = ?", [film_id]).fetchall()
        actors = cur.execute(f'SELECT * FROM actor join actor_film on actor.id == actor_film.actor_id where film_id={film_id}').fetchall()
        genres = cur.execute(f"SELECT * FROM genre_film where film_id={film_id}").fetchall()

    #result = get_db_result(f'SELECT * FROM film WHERE id={film_id}')
    #actors = get_db_result(f'SELECT * FROM actor join actor_film on actor.id == actor_film.actor_id where film_id={film_id}')
    #genres = get_db_result(f'SELECT * FROM genre_film where film_id={film_id}')
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