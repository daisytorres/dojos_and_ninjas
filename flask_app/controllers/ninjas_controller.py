from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.ninjas_model import Ninja
from flask_app.models.dojos_model import Dojo


#create route to display the form that will add a new ninja to a dojo
#this one does not call on the Ninja class so it does not need a classmethod
@app.route('/ninjas/new') #create route to DISPLAY adding a ninja to a list
def new_ninja():
    all_dojos=Dojo.get_all()
    return render_template("new_ninja.html", all_dojos=all_dojos) #this all_ninjas=all_ninjas allows us to have the option to select from our dojos in our database in this HTML template


#create route to take in the information you added
#create class for it (link should match the form action in your HTML)
@app.route('/ninja/create', methods=['POST']) #create route to DISPLAY adding a ninja to a list
def create_ninja():
    #for this one we will need a call to our ninja class to create a ninja from our request form above
    # Ninja.create(request.form) #the request form is the dicitonary that will fill out our query
    Ninja.create(request.form)
    return redirect (f'/dojos/{request.form["dojo_id"]}/view')

