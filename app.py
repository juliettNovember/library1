from flask import Flask, request, render_template, redirect, url_for, jsonify, abort, make_response
from forms import MovieForm
from models import projects


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/movlib/", methods=["GET", "POST"])
def projects_list():
    form = MovieForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            projects.create(form.data)
            # projects.save_all()
        return redirect(url_for("projects_list"))
    return render_template("movies.html", form=form, projects=projects.all(), error=error)
@app.route("/api/v1/movlib/<int:project_id>", methods=["GET"]) 
def get_project(project_id):
    project = projects.get(project_id)
    if not project:
        abort(404)
    return jsonify({"project": project})

@app.route("/api/v1/movlib/", methods=["POST"])
def create_project():
    project = {
        'id': projects.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json['description'],
        'year': request.json['year'],
        'species': request.json['species'],
        'watch': False
    }
    projects.create(project)
    return jsonify({'project': project}), 201

@app.route("/api/v1/movlib/<int:project_id>", methods=['DELETE'])
def delete_project(project_id):
    result = projects.delete(project_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/movlib/", methods=["GET"])
def projects_list_api_v1():
    return jsonify(projects.all())

@app.route("/movlib/<int:project_id>/", methods=["GET", "POST"])
def project_details(project_id):
    project = projects.get(project_id - 1)
    form = MovieForm(data=project)
    if request.method == "POST":
        if form.validate_on_submit():
            projects.update(tod_id - 1, form.data)
        return redirect(url_for("projects_list"))
    return render_template("project.html", form=form, project_id=project_id)

@app.route("/api/v1/movlib/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    project = projects.get(project_id)
    if not project:
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
    project = {
        'title': data.get('title', project['title']),
        'description': data.get('description', project['description']),
        'year': data.get('description', project['year']),
        'species': data.get('description', project['species']),
        'done': data.get('done', project['done'])
    }
    projects.update(project_id, project)
    return jsonify({'project': project})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
    app.run(debug=True)