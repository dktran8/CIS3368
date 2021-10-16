"""
Dinh Tran
CIS 3368
Professor Otto Dobretsberger
Final Project Sprint 1
"""

import mysql.connector
import flask
from flask import jsonify
from flask import request, make_response
from mysql.connector import Error
from sql1 import create_connection
from sql1 import execute_query
from sql1 import execute_read_query

#setting up an application name
app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show errors in browser

#Prints the entire guest table
@app.route('/guests', methods=['GET'])
def people():
    conn = create_connection("cis3368.cdqrwblrgkaj.us-east-2.rds.amazonaws.com", "schoolproject", "cis3368fall", "cis3368fall21")
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
    newfirstname = request_data['firstname']
    newlastname = request_data['lastname']
    newrestaurant = request_data['restaurantname']
    
    #connects to mySQL database and allows to add data from Postman to mySQL
    conn = create_connection("cis3368.cdqrwblrgkaj.us-east-2.rds.amazonaws.com", "schoolproject", "cis3368fall", "cis3368fall21")
    query = "INSERT INTO guest (firstname, lastname) VALUES ('%s', '%s')" % (newfirstname, newlastname)
    execute_query(conn,query)

    #make a while loop to ask user to input from 5 to 10 restaurants
    count = 0
    while (count <= 10):
        print("Type a list of restaurants with 5 being minimum and 10 beng maximum (Type 'Q' to quit): ")
        newrestaurant = input(" ")
        count += 1
        if newrestaurant == 'Q' :
            #keep asking for input if the numbers of restaurant is not enough
            if count < 5:
                print("You have to type at least 5 restaurants: ")
            #stop when enough restaurants
            else:
                break
        else:
            query2 = """INSERT INTO restaurant(restaurantname, guestid) VALUES ('%s', (SELECT max(id) FROM guest))""" % (newrestaurant)
            execute_query(conn, query2)
    return 'POST REQUEST WORKED'


#Delete a guest in the table
@app.route('/api/deleteguest', methods=['DELETE'])
def deleteguest():
    request_data = request.get_json()
    deletename = request_data['firstname']
    #connects to mySQL database and allows to modify data from Postman to mySQL
    conn = create_connection("cis3368.cdqrwblrgkaj.us-east-2.rds.amazonaws.com", "schoolproject", "cis3368fall", "cis3368fall21")
    query = "DELETE from guest WHERE firstname = '%s' " % (deletename)
    execute_query(conn,query)
    return 'Guest was successfully deleted.' #Returns a statement if the code works successfully

#Update a guest in the table
@app.route('/api/updateguest', methods=['PUT'])
def updateguest():
    request_data = request.get_json()
    guestid = request_data['id']
    updatefirstname = request_data['firstname']
    updatelastname = request_data['lastname']
    #connects to mySQL database and allows to modify data from Postman to mySQL
    conn = create_connection("cis3368.cdqrwblrgkaj.us-east-2.rds.amazonaws.com", "schoolproject", "cis3368fall", "cis3368fall21")
    query = "UPDATE guest SET firstname = '%s', lastname = '%s' WHERE id = %s" %(updatefirstname, updatelastname,guestid)
    execute_query(conn,query)
    return 'Guest was successfully updated'


#Print the entire restaurant table:
@app.route('/restaurants', methods=['GET'])
def place():
    conn = create_connection("cis3368.cdqrwblrgkaj.us-east-2.rds.amazonaws.com", "schoolproject", "cis3368fall", "cis3368fall21")
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
    conn = create_connection("cis3368.cdqrwblrgkaj.us-east-2.rds.amazonaws.com", "schoolproject", "cis3368fall", "cis3368fall21")
    query = "INSERT INTO restaurant (restaurantname) VALUES ('%s')" % (newname)
    execute_query(conn,query)
    return 'POST REQUEST WORKED'

#Delete a restaurant in the table
@app.route('/api/deleterestaurant', methods=['DELETE'])
def deleterestaurant():
    request_data = request.get_json()
    deletename = request_data['restaurantname']
    #connects to mySQL database and allows to modify data from Postman to mySQL
    conn = create_connection("cis3368.cdqrwblrgkaj.us-east-2.rds.amazonaws.com", "schoolproject", "cis3368fall", "cis3368fall21")
    query = "DELETE from restaurant WHERE restaurantname = '%s' " % (deletename)
    execute_query(conn,query)
    return 'Restaurant was successfully deleted.' #Returns a statement if the code works successfully

#Update a restaurant in the table
@app.route('/api/updaterestaurant', methods=['PUT'])
def updaterestaurant():
    request_data = request.get_json()
    restaurantid = request_data['id']
    updatename = request_data['restaurantname']
   
    #connects to mySQL database and allows to modify data from Postman to mySQL
    conn = create_connection("cis3368.cdqrwblrgkaj.us-east-2.rds.amazonaws.com", "schoolproject", "cis3368fall", "cis3368fall21")
    query = "UPDATE restaurant SET restaurantname= '%s' WHERE id = %s" %(updatename, restaurantid)
    execute_query(conn,query)
    return 'Restaurant was successfully updated'


#Generates a random restaurant
@app.route('/api/randomrestaurant', methods=["GET"])
def randomrestaurant():
    request_data = request.get_json()
    guestid = request_data['guestid']

    conn = create_connection("cis3368.cdqrwblrgkaj.us-east-2.rds.amazonaws.com", "schoolproject", "cis3368fall", "cis3368fall21")
    sql = "SELECT restaurantname FROM restaurant WHERE guestid = %s ORDER BY RAND () LIMIT 1" %(guestid)
    random_rest = execute_read_query(conn, sql)
    results = []
    for object in random_rest:
        results.append(object)
    return jsonify(results)

app.run()