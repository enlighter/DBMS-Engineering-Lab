import mysql.connector as mariadb

mariadb_connection = mariadb.connect(user='public', password='test3R', database='seleri')
cursor = mariadb_connection.cursor()

try:
	cursor.execute("select firstname, lastname from actors")
except mariadb.Error as error:
    print("Error: {}".format(error))

for first_name, last_name in cursor:
	print("First name: {}, Last name: {}".format(first_name,last_name))

#Actually commits the changes to the database
mariadb_connection.commit()