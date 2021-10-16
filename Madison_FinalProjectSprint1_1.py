
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
    
    count = 0
    # count how many restaurants the user adds
    while (count <= 9):
    #make a while loop to ask user to input from 5 to 10 restaurants
        print("Type a list of restaurants with 5 being minimum and 10 beng maximum (Type 'Q' to quit): ")
        newrestaurant = input(" ")
        if newrestaurant == 'Q' and count < 4:
            #keep asking for input if the numbers of restaurant is not enough
            #stop when enough restaurants or user has entered "Q"
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
    #connects to mySQL database and allows to modify data from Postman to mySQL
    conn = create_connection("cis3368fall2021.c2ksqbnomh6f.us-east-2.rds.amazonaws.com", "admin", "MadisonFall2021", "cis3368fall2021")
    if 'firstname' in request.args: #only if a firstname is provided as an argument, proceed
        firstname = str(request.args['firstname'])
    else:
        return 'ERROR: No ID provided!'
    sql = "SELECT * FROM guest"
    guest = execute_read_query(conn, sql)
    results = []

    for user in guest:
        if user['firstname'] == firstname:
            results.append(user['id'])
            # if the name the user entered is in the guest table it will add the ID to the results list
            query = "DELETE from guest WHERE firstname = '%s' " % (firstname)  # Deletes the guest and their information from guest table
            execute_query(conn,query)
            sql2 = "SELECT * FROM restaurant"
            rest = execute_read_query(conn, sql2)
            for new in rest: # goes through the restaurant table 
                for x in results: # goes through the results list (which should only have the ID of the guest that was just deleted)
                    if new['guestid'] == x: 
                        # if the guest id from the restaurant table and the ID of the guest that was just deleted match
                        # It deletes all the restaurants that that guest had enetered
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

#Update a restaurant in the table
@app.route('/api/updaterestaurant', methods=['PUT'])
def updaterestaurant():
    request_data = request.get_json()
    restaurantid = request_data['id']
    updatename = request_data['restaurantname']
   
    #connects to mySQL database and allows to modify data from Postman to mySQL
    conn = create_connection("cis3368fall2021.c2ksqbnomh6f.us-east-2.rds.amazonaws.com", "admin", "MadisonFall2021", "cis3368fall2021")
    query = "UPDATE restaurant SET restaurantname= '%s' WHERE id = %s" %(updatename, restaurantid)
    execute_query(conn,query)
    return 'Restaurant was successfully updated'

@app.route('/api/randomrestaurant', methods=["GET"])
def randomrestaurant():
    conn = create_connection("cis3368fall2021.c2ksqbnomh6f.us-east-2.rds.amazonaws.com", "admin", "MadisonFall2021", "cis3368fall2021")
    print("How many people are going to dinner?")
    dinner = int(input(""))
    list = []
    for x in range(dinner): # loops through asking for user first and last name for each person attending dinner
        print("Please enter your first name:")
        selectf = input(" ")
        list.append(selectf)
        print("Please enter your lastname:")
        selectl = input(" ")   
        list.append(selectl) 
    # the name of the people attending dinner are all added into a list
    sql = "SELECT * FROM guest"
    guest = execute_read_query(conn, sql)
    results = []
    for user in guest:
        for x in list: # the for loop goes through the list of people attending dinner
            # if those names are in the guest table it adds their ID number to a new list
            if x in user['firstname'] or x in user['lastname']:
                results.append(user['id'])
                sql2 = "SELECT * FROM restaurant"
                rest = execute_read_query(conn, sql2)
                for new in rest: # goes through the restaurant table 
                    for x in results: # goes through the results list (which should only have the ID of the guests that were entered)
                        if new['guestid'] == x: 
                            # if the ID's from the results list match the guest ID's from the restaurant list
                            # it takes the restaurants of all the guests that were entered and put it into another empty list
                            sql3 = f"""SELECT restaurantname FROM restaurant WHERE guestid = {x} ORDER BY RAND () LIMIT 1"""  
                            # ^ selects a random restauramt from the restaurant list of the people going to dinner
                            random_rest = execute_read_query(conn, sql3)
                            results2 = []
                        for object in random_rest:
                            results2.append(object)
                        return jsonify(results2)

app.run()
