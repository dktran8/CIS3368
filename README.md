# CIS3368
#Dinh Tran
#Madison Fletcher


# Notes:
#When running the /api/addguest endpoint, enter the input for customer lastname, firstname and the name of restaurant in Postman and click send. A loop will appear in VScode terminal so that you can keep adding restaurants in the database (5 minimum and 10 maximum). Hit "Q" when done and the name of the guest will be added into the guest table and the name of the restaurant as well as the id of the customer will be added into the restaurant table.

#When running the /api/deleteguest endpoint, enter "firstname" as the KEY and the customer name as the VALUE in Params in Postman and then click send. The customer name as well as his/her restaurants will be deleted from guest and restaurant tables.

#When running the /api/updateguest endpoint,enter "id" : "(value)", "firstname" : "(value)" and "lastname" : "(value)" in Body in Postman and click send, the user information will be updated.

#When running the /api/addrestaurant endpoint,enter "restaurantname" : "(value)" in Body in Postman and click send, the new restaurant will be added.

#When running the /api/deleterestaurant endpoint,enter "restaurantname" : "(value)" in Body in Postman and click send, the new restaurant will be added.

#When running the /api/updaterestaurant endpoint,enter "id" : "(value)", "restaurantname" : "(value)" in Body in Postman and click send, the restaurant information will be updated.
