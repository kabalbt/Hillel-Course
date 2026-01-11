import functools
import os
from dateutil import parser

from sqlalchemy import select, update, func

import database
import models

from flask import Flask, session, render_template, url_for, redirect, jsonify
from flask import request
import sqlite3



app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def decorator_check_login(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user_login'))
    return wrapper

@app.route('/')
@decorator_check_login
def main_page():

    database.init_db()
    smth = select(models.Film).limit(10).order_by(models.Film.added_at.desc())
    data = database.db_session.execute(smth).fetchall()
    data2 = [itm[0] for itm in data]

    return render_template('main.html', films=data2)

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
    birth_date = parser.parse(request.form['birth_date'])

    database.init_db()

    new_user = models.User(first_name=first_name, last_name=last_name, password=password, login=login, email=email, birth_date=birth_date)

    database.db_session.add(new_user)
    database.db_session.commit()

    return 'Register'

@app.route('/login', methods=['GET'])
def user_login():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def user_login_post():
    login = request.form['login']
    password = request.form['password']


    database.init_db()

    stmt = select(models.User).where(models.User.login == login, models.User.password == password)
    data = database.db_session.execute(stmt).fetchall()
    if data:
        user_obj = data[0][0]

    result = database.db_session.query(models.User).filter_by(login=login, password=password).first()


    if result:
        session['logged_in'] = True
        session['user_id'] = result.id
        return f'Login with user {result}'
    return 'Login failed'



@app.route('/logout', methods=['GET'] )
@decorator_check_login
def user_logout():
    session.clear()
    return 'logout'

@app.route('/user/<user_id>', methods=['GET', 'POST'])
def user_profile(user_id):
    database.init_db()
    session_user_id = session.get('user_id')
    if request.method == 'POST':
        if int(user_id) != session_user_id:
            return "You can edit only your profile"

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        birth_date = parser.parse(request.form['birth_date'])
        phone_number = request.form['phone_number']
        photo = request.form['photo']
        additional_info = request.form['additional_info']

        stmt = update(models.User).where(models.User.id == user_id).values(first_name=first_name, last_name=last_name, email=email, password=password, birth_date=birth_date, phone_number=phone_number, photo=photo, additional_info=additional_info)
        database.db_session.execute(stmt)
        database.db_session.commit()
        return f'User {user_id} updated'

    else:

        query_user_by_id = select(models.User).where(models.User.id == user_id)
        user_by_id =database.db_session.execute(query_user_by_id).scalar_one()

        if session_user_id is None:
            user_by_session = "No user in session"
        else:
            query_user_by_session = select(models.User).where(models.User.id == session_user_id)
            user_by_session = database.db_session.execute(query_user_by_session).scalar_one()

        database.db_session.commit()
    return render_template("user_page.html", user=user_by_id, user_session=user_by_session)



@app.route('/user/<user_id>/delete', methods=['GET'])
def user_delete(user_id):
    session_user_id = session.get('user_id')
    if user_id == session_user_id:
        return f'User {user_id} deleted'
    else:
        return 'You can delete only your profile'

@app.route('/films', methods=['GET'])
@decorator_check_login
def films():
    filter_params = request.args
    filter_list_texts = []
    films_query = select(models.Film)
    for key, value in filter_params.items():
        if value:
            if key == 'name':
                films_query = films_query.where(models.Film.name.like(f'%{value}%'))
            elif key == 'rating':
                value = float(value)
                films_query = films_query.where(models.Film.rating == value)
            elif key == 'country':
                films_query = films_query.where(models.Film.country == value)
            elif key == 'year':
                films_query = films_query.where(models.Film.year == int(value))

    films = films_query.order_by(models.Film.added_at.desc())
    result_films = database.db_session.execute(films).scalars()
    countries = select(models.Country)
    result_countries = database.db_session.execute(countries).scalars()

    return render_template('films.html', films=result_films, countries = result_countries)

@app.route('/films', methods=['POST'])
@decorator_check_login
def film_add():
    database.init_db()

    data = request.get_json() or {}
    name = data.get('name')
    poster = data.get('poster')
    description = data.get('description')
    rating = data.get('rating')
    country = data.get('country')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    new_film = models.Film(name=name, poster=poster, description=description, rating=rating, country=country)
    result = database.db_session.add(new_film)
    database.db_session.commit()

    return  jsonify({'films_id': new_film.id}), 201

@app.route('/films/<int:film_id>', methods=['GET'])
def film_info(film_id):
    database.init_db()

    film_by_id = select(models.Film).where(models.Film.id == film_id)
    result_film_by_id = database.db_session.execute(film_by_id).scalar_one()

    actors = select(models.Actor).join(models.Actorfilm, models.Actor.id == models.Actorfilm.actor_id).where(models.Actorfilm.film_id == film_id)
    result_actors = database.db_session.execute(actors).scalars()

    genres = select(models.Genre).join(models.GenreFilm, models.Genre.genre == models.GenreFilm.genre_id).where(models.GenreFilm == film_id)
    result_genres = database.db_session.execute(genres).scalars()


    return jsonify({
        'id': result_film_by_id.id,
        'name': result_film_by_id.name,
        'poster': result_film_by_id.poster,
        'description': result_film_by_id.description,
        'rating':result_film_by_id.rating,
        'country': result_film_by_id.country,
        'added_at': result_film_by_id.added_at,
        'actors': [itm.to_dict() for itm in result_actors],
        'genres': [itm.to_dict() for itm in result_genres]
    })

@app.route('/films/<int:film_id>', methods=['PUT'])
@decorator_check_login
def film_update(film_id):
    data = request.get_json() or {}
    database.init_db()

    new_film_query = select(models.Film).where(models.Film.id == film_id)
    new_film = database.db_session.execute(new_film_query).scalar_one()

    new_film.name = data.get("name")
    new_film.poster = data.get("poster")
    new_film.description = data.get("description")
    new_film.rating = data.get("rating")
    new_film.country = data.get("country")

    database.db_session.add(new_film)
    database.db_session.commit()

    return jsonify({"film_id": film_id})

@app.route('/films/<film_id>', methods=['DELETE'])
def film_delete(film_id):
    return f'film {film_id} deleted'

@app.route('/films/search', methods=['GET'])
def films_search():
    name = request.args.get('name', '')

    database.init_db()

    film_search_query = select(models.Film).where(models.Film.name.like(f'%{name}%')).order_by(models.Film.added_at.desc())
    result_film_search = database.db_session.execute(film_search_query).scalars()

    return jsonify([itm.to_dict() for itm in result_film_search])


@app.route('/films/<int:film_id>/rating', methods=['GET'])
def film_rating_info(film_id):
    database.init_db()

    ratings_query = select(models.Feedback).where(models.Feedback.film == film_id)
    ratings = database.db_session.execute(ratings_query).scalars()

    grades_query = select(func.avg(models.Feedback.grade).label('average'), func.count(models.Feedback.id).label('ratings_count'))
    grades = database.db_session.execute(grades_query).fetchone()

    return jsonify({
        "film_id": film_id,
        "average_rating": grades[0],
        "ratings_count": grades[1],
        "ratings": ratings
    })

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