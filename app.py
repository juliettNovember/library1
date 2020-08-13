from flask import Flask, request, render_template, redirect, url_for, jsonify, abort, make_response
from forms import MovieForm
from models import movlib


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/", methods=["GET"])
def redirections():
    return redirect("/movies/")

@app.route("/movies/", methods=["GET", "POST"])
def movies_list():
    movlib.create_movie_entry()   
    form = MovieForm()
    error = ""
    if request.method == "POST":       
        if form.validate_on_submit():    
            movlib.create(form.data)    
        return redirect(url_for("movies_list"))
    return render_template("movies.html", form=form, movlib=movlib.all(), error=error)


@app.route("/movies/<int:id>", methods=["GET", "POST"])
def movie_details(id):
    movie = movlib.details(id)
    form = MovieForm(data=movie)
    if request.method == "POST":
        if form.validate_on_submit(): 
            print(form)   
            movlib.update(id, form.data)  
        return redirect("/movies/")
    return render_template("update.html", movie=movie, form=form)

@app.route("/movies/delete/<int:id>", methods=["GET"])
def movie_delete(id):
    result = movlib.delete((id))
    return redirect("/movies/")

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
    app.run(debug=True)