from flask import Flask


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/register', methods=['POST'])
def user_register():
    return 'register'

@app.post('/login', )
def user_login():
    return 'login'

@app.post('/logout', methods=['GET'])
def user_logout():
    return 'logout'

@app.route('/user/<user_id>', methods=['GET', 'PATCH'])
def user_profile(user_id):
    return f'User {user_id}'


@app.route('/user/<user_id>', methods=['DELETE'])
def user_delete(user_id):
    return f'User {user_id} deleted'

@app.route('/films', methods=['GET'])
def films():
    return (
        "Films list:\n"
        "1. The Shawshank Redemption\n"
        "2. The Godfather\n"
        "3. The Dark Knight\n"
    )

@app.route('/films', methods=['POST'])
def film_add():
    return 'films added'

@app.route('/films/<film_id>', methods=['GET'])
def film_get(film_id):
    return f'Film {film_id}'

@app.route('/films/<film_id>', methods=['PUT'])
def film_update(film_id):
    return f'film {film_id} updated'

@app.route('/films/<film_id>', methods=['DELETE'])
def film_delete(film_id):
    return f'film {film_id} deleted'

@app.route('/films/<film_id>/rating', methods=['GET'])
def film_rating(feedback_id):
    return f'film {feedback_id} rating'

@app.route('/films/<film_id>/rating', methods=['POST'])
def film_rating(film_id):
    return f'film {film_id} rated'

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