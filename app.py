from flask import Flask, request, render_template, redirect, url_for, jsonify, abort, make_response
from forms import MovieForm
from models import movies


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/movlib/", methods=["GET", "POST"])
def movies_list():
    form = MovieForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            movies.create(form.data)
            movies.save_all()
        return redirect(url_for("movies_list"))

    return render_template("movies.html", form=form, movies=movies.all(), error=error)

@app.route("/api/v1/movlib/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    todo = movies.get(movie_id)
    if not movie:
        abort(404)
    return jsonify({"movie": movie})

@app.route("/api/v1/movlib/", methods=["POST"])
def create_movie():
    movie = {
        'id': movies.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json['description'],
        'year': request.json['year'],
        'species': request.json['species'],
        'watch': False
    }
    movies.create(movie)
    return jsonify({'movie': movie}), 201

@app.route("/api/v1/movlib/<int:movie_id>", methods=['DELETE'])
def delete_movie(movie_id):
    result = movies.delete(movie_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/movlib/", methods=["GET"])
def movies_list_api_v1():
    return jsonify(movies.all())

@app.route("/movlib/<int:todo_id>/", methods=["GET", "POST"])
def movie_details(todo_id):
    movie = movies.get(todo_id - 1)
    form = MovieForm(data=movie)

    if request.method == "POST":
        if form.validate_on_submit():
            todos.update(movie_id - 1, form.data)
        return redirect(url_for("movies_list"))
    return render_template("movies.html", form=form, movie_id=movie_id)

@app.route("/api/v1/movlib/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    movie = movies.get(movie_id)
    if not movie:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'year' in data and not isinstance(data.get('year'), str),
        'species' in data and not isinstance(data.get('species'), str),
        'done' in data and not isinstance(data.get('done'), bool)
    ]):
        abort(400)
    movie = {
        'title': data.get('title', movie['title']),
        'description': data.get('description', movie['description']),
        'year': data.get('description', movie['year']),
        'species': data.get('description', movie['species']),
        'done': data.get('done', movie['done'])
    }
    movies.update(movie_id, movie)
    return jsonify({'movie': movie})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
    app.run(debug=True)