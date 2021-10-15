
# Dinh Tran
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
    query2 = """INSERT INTO restaurant(restaurantname, guest_id) VALUES ('%s', (SELECT max(id) FROM guest))""" % (newrestaurant)
    execute_query(conn, query2)
    return 'POST REQUEST WORKED'


#Delete a guest in the table
@app.route('/api/deleteguest', methods=['DELETE'])
def deleteguest():
    request_data = request.get_json()
    deletename = request_data['firstname']
    #connects to mySQL database and allows to modify data from Postman to mySQL
    conn = create_connection("cis3368fall2021.c2ksqbnomh6f.us-east-2.rds.amazonaws.com", "admin", "MadisonFall2021", "cis3368fall2021")
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
    conn = create_connection("cis3368fall2021.c2ksqbnomh6f.us-east-2.rds.amazonaws.com", "admin", "MadisonFall2021", "cis3368fall2021")
    query = "UPDATE guest SET firstname = '%s', lastname = '%s' WHERE id = %s" %(updatefirstname, updatelastname,guestid)
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



app.run()