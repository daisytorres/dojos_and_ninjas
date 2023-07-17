from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE


#this brings a function init that connects to mysqlconnection connection and passes a database through it
# and creates an instance where we can call query_db

#creating a class for each table and it's attributes. Take in a dictionary so that the results 
#can become a list of dictionaires where we can make instances out of it
class Ninja: 
    def __init__(self, data): 
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.dojo_id = data['dojo_id']


#Write class methods so that you can create, read, update, and delete objects w/o having to instantiate them
#You want to be able to call them from the (ninja) class itself 
#(gets all of the ninjas and sends them all back as ninja objects)
    @classmethod
    def get_all(cls):
        #run a query from SQL (database)
        query = """
            SELECT * FROM ninjas;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        all_ninjas = [] #We then need to turn them into ninja objects by creating an empty list (instantiating objects)
        for row_from_db in results: #from iterative VARIABLE (we can make up) row_from_db is what it represents (each row from the dict) and results is the list of dictionaries
            ninja_instance = cls(row_from_db) #then we want to make a ninja instance from that row by passing it to our class - cls(aka referring to Ninja) from that row
            all_ninjas.append(ninja_instance) #then we are going to put that instance to our all_ninjas
        return all_ninjas #then we want it returned



    #create a route for this in controller, then come back and create it's class
    #INSERT queries will return the ID NUMBER of the row inserted
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO ninjas (first_name, last_name, age, dojo_id)
            VALUES (%(first_name)s,%(last_name)s,%(age)s,%(dojo_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)
    #make sure you add to correct route with request.form
    