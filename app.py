from flask import Flask, request, render_template, redirect, url_for, jsonify, abort, make_response
from forms import TodoForm
from models import todos


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/movlib/", methods=["GET", "POST"])
def todos_list():
    form = TodoForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            todos.create(form.data)
            todos.save_all()
        return redirect(url_for("todos_list"))

    return render_template("todos.html", form=form, todos=todos.all(), error=error)

@app.route("/api/v1/movlib/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    return jsonify({"todo": todo})

@app.route("/api/v1/movlib/", methods=["POST"])
def create_todo():
    todo = {
        'id': todos.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json['description'],
        'year': request.json['year'],
        'species': request.json['species'],
        'watch': False
    }
    todos.create(todo)
    return jsonify({'todo': todo}), 201

@app.route("/api/v1/movlib/<int:todo_id>", methods=['DELETE'])
def delete_todo(todo_id):
    result = todos.delete(todo_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/movlib/", methods=["GET"])
def todos_list_api_v1():
    return jsonify(todos.all())

@app.route("/movlib/<int:todo_id>/", methods=["GET", "POST"])
def todo_details(todo_id):
    todo = todos.get(todo_id - 1)
    form = TodoForm(data=todo)

    if request.method == "POST":
        if form.validate_on_submit():
            todos.update(tod_id - 1, form.data)
        return redirect(url_for("todos_list"))
    return render_template("todo.html", form=form, todo_id=todo_id)

@app.route("/api/v1/movlib/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
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
    todo = {
        'title': data.get('title', todo['title']),
        'description': data.get('description', todo['description']),
        'year': data.get('description', todo['year']),
        'species': data.get('description', todo['species']),
        'done': data.get('done', todo['done'])
    }
    todos.update(todo_id, todo)
    return jsonify({'todo': todo})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
    app.run(debug=True)