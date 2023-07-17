from flask_app import app
from flask import render_template, redirect, request, request
from flask_app.models.dojos_model import Dojo #this imports the class created in dojos_model from class method


# class method to get all dojos for our list
@app.route('/dojos')
def all_dojos():
    all_dojos = Dojo.get_all()
    return render_template('index.html', all_dojos=all_dojos) #STEP 4, create render_template (and add to top) and create variable all_dojos=all_dojos for your jinja


# class method for adding a new Dojo
@app.route('/dojos/new', methods = ['POST'])
def create_dojo():
    data = {
        "name": request.form["name"]
    }
    id = Dojo.create(data)
    return redirect ('/dojos')

@app.route('/dojos/<int:id>/view')
def view_one_dojo(id):
#then we are going to need a get_one function, that gets us that one Dojo
#since it is one_dojo, we are going to need to query it's ID (where id =) 
# a data dictionary to pass through that query making sure it has a key of 'id' and the id value we want it to habe
    data = {
        'id': id
    }
    one_dojo = Dojo.get_dojo_with_ninjas(data)
    return render_template("one_dojo.html", one_dojo=one_dojo)
