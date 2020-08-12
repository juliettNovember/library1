from flask import Flask, request, render_template, redirect, url_for, jsonify, abort, make_response
from forms import MovieForm
from models import movlib


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/movlib/", methods=["GET", "POST"])
def movlib_list():
    movlib.create_movie_entry()   
    form = MovieForm()
    error = ""
    if request.method == "POST":
        movlib.delete((request.form.get('deleteid')))
        if form.validate_on_submit():    
            movlib.create(form.data)    
        return redirect(url_for("movlib_list"))
    return render_template("movies.html", form=form, movlib=movlib.all(), error=error)

@app.route("/movlib/<int:id>", methods=["GET", "POST"])
def update_project(id):
    movie = movlib.details(id)
    form = MovieForm(data=movie)
    if request.method == "POST":
        movlib.delete((request.form.get('deleteid')))
        if form.validate_on_submit():    
            movlib.create(form.data)  
        return redirect(url_for("movlib_list"))
    return render_template("movies.html", movie=movie, form=form)


@app.route("/movlib/delete<int:project_id>", methods=['GET'])
def delete_project(project_id):
    result = movlib.delete((project_id))
    if not result:
        abort(404)
    return redirect("/movlib/")

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
    app.run(debug=True)