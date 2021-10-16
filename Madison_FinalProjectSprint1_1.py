
# Dinh Tran
# Madison Fletcher
# CIS 3368
# Professor Otto Dobretsberger
# Final Project Sprint 1


import mysql.connector
import flask
from flask import jsonify
from flask import request, make_response
from mysql.connector import Error
from sql import create_connection
from sql import execute_query
from sql import execute_read_query

#setting up an application name
app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show errors in browser

#Prints the entire guest table
@app.route('/guests', methods=['GET'])
def people():
    conn = create_connection("cis3368fall2021.c2ksqbnomh6f.us-east-2.rds.amazonaws.com", "admin", "MadisonFall2021", "cis3368fall2021")
    #Selects all data from the table
    sql = "SELECT * FROM guest"
    guest = execute_read_query(conn,sql)
    #Results all data to return
    results = []
    for people in guest:
        results.append(people)
    return jsonify(results)

#Add a new guest to the table
@app.route('/api/addguest', methods=['POST'])
#Request data to be added
def addguest():
    request_data = request.get_json()
    # guestid = request_data['id']
    newfirstname = request_data['firstname']
    newlastname = request_data['lastname']
    newrestaurant = request_data['restaurantname']
 
    #connects to mySQL database and allows to add data from Postman to mySQL
    conn = create_connection("cis3368fall2021.c2ksqbnomh6f.us-east-2.rds.amazonaws.com", "admin", "MadisonFall2021", "cis3368fall2021")
    query = "INSERT INTO guest (firstname, lastname) VALUES ('%s', '%s')" % (newfirstname, newlastname)
    execute_query(conn,query)
    #make a while loop to ask user to input from 5 to 10 restaurants
    count = 0
    while (count <= 9):
        print("Type a list of restaurants with 5 being minimum and 10 beng maximum (Type 'Q' to quit): ")
        newrestaurant = input(" ")
        if newrestaurant == 'Q' and count < 4:
            #keep asking for input if the numbers of restaurant is not enough
            #stop when enough restaurants
            print("You have to type at least 5 restaurants: ")
        elif newrestaurant == 'Q' and count > 4:
            break
        else:
            # after for asking for 5 - 10 restaurants, the query will insert the restaurant name and guest id into the restaurant table
            # the code adds the largest id from the guest table, and since the query before this adds a guest to the guest table the guest 
            # with the largest id will be the last guest added.
            query2 = f"""INSERT INTO restaurant (restaurantname, guestid) VALUES ("{newrestaurant}", (SELECT max(id) from guest))"""""
            execute_query(conn, query2)
            count = count + 1
    return 'POST REQUEST WORKED'


#Delete a guest in the table
@app.route('/api/deleteguest', methods=['GET'])
def deleteguest():
    request_data = request.get_json()
    deletename = request_data['firstname']
    # id = request_data['id']
    #connects to mySQL database and allows to modify data from Postman to mySQL
    conn = create_connection("cis3368fall2021.c2ksqbnomh6f.us-east-2.rds.amazonaws.com", "admin", "MadisonFall2021", "cis3368fall2021")
    if 'firstname' in request.args: #only if an id is provided as an argument, proceed
        firstname = str(request.args['firstname'])
    else:
        return 'ERROR: No ID provided!'
    sql = "SELECT * FROM guest"
    guest = execute_read_query(conn, sql)
    results = []

    for user in guest:
        if user['firstname'] == firstname:
            results.append(user['id'])
            query = "DELETE from guest WHERE firstname = '%s' " % (firstname)
            execute_query(conn,query)
            sql2 = "SELECT * FROM restaurant"
            rest = execute_read_query(conn, sql2)
            for new in rest:
                for x in results:
                    if new['guestid'] == x:
                        query2 = f"""DELETE from restaurant WHERE guestid = {x}"""
                        execute_query(conn,query2)
    return 'Guest was successfully deleted.' #Returns a statement if the code works successfully


#Update a guest in the table
@app.route('/api/updateguest', methods=['PUT'])
def updateguest():
    request_data = request.get_json()
    guestid = request_data['id']
    updatefirstname = request_data['firstname']
    updatelastname = request_data['lastname']
    #connects to mySQL database and allows to modify data from Postman to mySQL
    conn = create_connection("cis3368fall2021.c2ksqbnomh6f.us-east-2.rds.amazonaws.com", "admin", "MadisonFall2021", "cis3368fall2021")
    query = "UPDATE guest SET firstname = '%s', lastname = '%s' WHERE id = %s" %(updatefirstname, updatelastname, guestid)
    execute_query(conn,query)
    return 'Guest was successfully updated'


#Print the entire restaurant table:
@app.route('/restaurants', methods=['GET'])
def place():
    conn = create_connection("cis3368fall2021.c2ksqbnomh6f.us-east-2.rds.amazonaws.com", "admin", "MadisonFall2021", "cis3368fall2021")
    #Selects all data from the table
    sql = "SELECT * FROM restaurant"
    restaurant = execute_read_query(conn,sql)
    #Results all data to return
    results = []
    for place in restaurant:
        results.append(place)
    return jsonify(results)

#Add a new restaurant to the table
@app.route('/api/addrestaurant', methods=['POST'])
#Request data to be added
def addrestaurant():
    request_data = request.get_json()
    newname = request_data['restaurantname']
    
    #connects to mySQL database and allows to add data from Postman to mySQL
    conn = create_connection("cis3368fall2021.c2ksqbnomh6f.us-east-2.rds.amazonaws.com", "admin", "MadisonFall2021", "cis3368fall2021")
    query = "INSERT INTO restaurant (restaurantname) VALUES ('%s')" % (newname)
    execute_query(conn,query)
    return 'POST REQUEST WORKED'

#Delete a restaurant in the table
@app.route('/api/deleterestaurant', methods=['DELETE'])
def deleterestaurant():
    request_data = request.get_json()
    deletename = request_data['restaurantname']
    #connects to mySQL database and allows to modify data from Postman to mySQL
    conn = create_connection("cis3368fall2021.c2ksqbnomh6f.us-east-2.rds.amazonaws.com", "admin", "MadisonFall2021", "cis3368fall2021")
    query = "DELETE from restaurant WHERE restaurantname = '%s' " % (deletename)
    execute_query(conn,query)
    return 'Restaurant was successfully deleted.' #Returns a statement if the code works successfully

#Generates a random restaurant
@app.route('/api/randomrestaurant', methods=["GET"])
def randomrestaurant():
    conn = create_connection("cis3368.cdqrwblrgkaj.us-east-2.rds.amazonaws.com", "schoolproject", "cis3368fall", "cis3368fall21")
    sql = "SELECT restaurantname FROM restaurant ORDER BY RAND () LIMIT 5"
    random_rest = execute_read_query(conn, sql)
    results = []
    for object in random_rest:
        results.append(object)
    return jsonify(results)


app.run()
