from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
#this brings a function init that connects to mysqlconnection connection and passes a database through it
# and creates an instance where we can call query_db
from flask_app.models import ninjas_model

#step 1: creating a class for each table and it's attributes. Creating a dictionary so that the results 
#can become a list of dictionaires where we can make instances out of it
class Dojo: 
    def __init__(self, data): 
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.ninjas = [] #list of ninjas when we show the dojo page
        

#STEP 2: Write class methods so that you can create, read, update, and delete objects w/o having to instantiate them
#You want to be able to call them from the (dojo) class itself 
#(gets all of the dojos and sends them all back as dojo objects)
    @classmethod
    def get_all(cls):
        #run a query from SQL (database)
        query = """
            SELECT * FROM dojos;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        all_dojos = [] #We then need to turn them into dojo objects by creating an empty list (instantiating objects)
        for row_from_db in results: #from iterative VARIABLE (we can make up) row_from_db is what it represents (each row from the dict) and results is the list of dictionaries
            dojo_instance = cls(row_from_db) #then we want to make a dojo instance from that row by passing it to our class - cls(aka referring to Dojo) from that row
            all_dojos.append(dojo_instance) #then we are going to put that instance to our all_dojos
        return all_dojos #then we want it returned
    
    # create a route for this in controller, then come back and create it's class
    #INSERT queries will return the ID NUMBER of the row inserted 
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO dojos (name, created_at, updated_at)
            VALUES (%(name)s, NOW(), NOW());
        """
        #this is getting all of our values and turning them into strings/input value and not part of query
        return connectToMySQL(DATABASE).query_db(query,data)
    #make sure you add to correct route with request.form

    @classmethod
    def get_one(cls, data):
        query="""
            SELECT * FROM dojos WHERE id =%(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            dojo_instance = cls(results[0]) #we pass index 0 because we know if this statement is true, it is the first index of the returned list (should be only)
            return dojo_instance
        return results #if we do not have a result/matching id, we want results returned of what we do get to figure out error


    @classmethod
    def get_dojo_with_ninjas(cls, data):
        query="""
            SELECT * FROM dojos LEFT JOIN ninjas ON dojos.id = ninjas.dojo_id  
            WHERE dojos.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        #each dictionary is going to have the same for the id from dojos, so we can create our Dojo object off the results so we keep the instance below
        if results:
            dojo_instance = cls(results[0]) 
            ninjas_list = [] 
            for row in results: #then we want to iterate over the results
                ninja_data = {
                    'id': row['ninjas.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'age': row['age'],
                    'created_at': row['ninjas.created_at'],
                    'updated_at': row['ninjas.updated_at'],
                    'dojo_id': row['dojo_id']
                }
                ninjas_instance = ninjas_model.Ninja(ninja_data) #if you are brining another class in the model, you need to bring in the whole file to avoid circular imports (in controller can just use Dojo. or Ninja.)
                ninjas_list.append(ninjas_instance)
            dojo_instance.all_ninjas = ninjas_list #you can make a new attribute for a new instance whenever you want. So the dojo_instance we created above has a brand new insrance where we are generating the ninjas list
            return dojo_instance
        return results 
