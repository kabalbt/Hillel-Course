from flask import Flask, session, render_template
from flask import request
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def film_dictionary(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class db_connection:
    def __init__(self):
        self.conn = sqlite3.connect('hw2.db')
        self.conn.row_factory = film_dictionary
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


def get_db_result(query):
    conn = sqlite3.connect('hw2.db')
    conn.row_factory = film_dictionary
    cur = conn.cursor()
    res = cur.execute(query)
    result = res.fetchall()
    conn.close()
    return result

@app.route('/')
def main_page():
    with db_connection() as cur:
        result = cur.execute('SELECT * FROM film order by added_at DESC limit 10').fetchall()

    # result = get_db_result('SELECT * FROM film order by added_at DESC limit 10')
    return render_template('main.html', films=result)

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')




@app.route('/register', methods=['POST'])
def user_register():
    first_name = request.form['fname']
    last_name = request.form['lname']
    password = request.form['password']
    login = request.form['login']
    email = request.form['email']
    birth_date = request.form['birth_date']
    with db_connection() as cur:
        cur.execute("INSERT INTO user(first_name, last_name, password, login, email, birth_date) VALUES (?, ?, ?, ?, ?, ?)",
                    (first_name, last_name, password, login, email, birth_date))
    return 'Register'

@app.route('/login', methods=['GET'])
def user_login():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def user_login_post():
    login = request.form['login']
    password = request.form['password']
    with db_connection() as cur:
        cur.execute("SELECT * FROM user WHERE login=? AND password=?", (login, password))
        result = cur.fetchone()
    if result:
        session['logged_in'] = True
        session['user_id'] = result['id']
        return f'Login with user {result}'
    return 'Login failed'



@app.route('/logout', methods=['GET'] )
def user_logout():
    session.clear()
    return 'logout'

@app.route('/user/<user_id>', methods=['GET', 'POST'])
def user_profile(user_id):
    session_user_id = session.get('user_id')
    if request.method == 'POST':
        if int(user_id) != session_user_id:
            return "You can edit only your profile"

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        birth_date = request.form['birth_date']
        phone_number = request.form['phone_number']
        photo = request.form['photo']
        additional_info = request.form['additional_info']
        with db_connection() as cur:
            cur.execute(f'UPDATE user SET first_name="{first_name}", last_name="{last_name}", email="{email}", password="{password}", birth_date="{birth_date}", phone_number="{phone_number}", photo="{photo}", additional_info="{additional_info}" WHERE id={user_id}')

        return f'User {user_id} updated'
    else:
        with db_connection() as cur:
            cur.execute(f"SELECT * FROM user WHERE id={user_id}")
            user_by_id = cur.fetchone()

            if session_user_id is None:
                user_by_session = "No user in session"
            else:
                cur.execute(f"SELECT * FROM user WHERE id={session_user_id}")
                user_by_session = cur.fetchone()
        return render_template("user_page.html", user=user_by_id, user_by_session=user_by_session)
        #return f'You logged in as  {user_by_session}, user {user_id} data: {user_by_id}'


@app.route('/user/<user_id>/delete', methods=['GET'])
def user_delete(user_id):
    session_user_id = session.get('user_id')
    if user_id == session_user_id:
        return f'User {user_id} deleted'
    else:
        return 'You can delete only your profile'

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
        result = get_db_result(f'SELECT * FROM film WHERE id={film_id}')
        actors = get_db_result(f'SELECT * FROM actor join actor_film on actor.id == actor_film.actor_id where film_id={film_id}')
        genres = get_db_result(f'SELECT * FROM genre_film where film_id={film_id}')
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