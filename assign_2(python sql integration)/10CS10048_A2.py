import mysql.connector as mariadb
from pprintpp import pprint

''' to run:
i)
>select title, year from starred, movies where starred.MRN = movies.MRN and starred.A_ID in ( select A_ID from actors where actors.firstname="Shahrukh" and actors.lastname="Khan" );

ii)
>select title, year from starred, movies where starred.MRN = movies.MRN and starred.A_ID in (select a.A_ID from actors as a where a.firstname="Shahrukh" and a.lastname="Khan") and movies.MRN in (select directed.MRN from directed, movies where directed.MRN = movies.MRN and directed.D_ID in (select directors.D_ID from directors where directors.firstname="Shahrukh" and directors.lastname="Khan"));

iii)
>select title, year, genre from starred, movies where starred.MRN=movies.MRN and starred.A_ID in (select a.A_ID from actors as a where a.firstname="Shahrukh" and a.lastname="Khan") and movies.genre="thriller" and year>2000;

iv)
>select actors.firstname, actors.lastname from actors, starred where actors.A_ID=starred.A_ID and starred.MRN in (select starred.MRN from starred, movies where starred.MRN=movies.MRN and starred.A_ID in (select a.A_ID from actors as a where a.firstname="Shahrukh" and a.lastname="Khan")) and starred.A_ID not in (select a.A_ID from actors as a where a.firstname="Shahrukh" and a.lastname="Khan") and actors.A_ID in (select b.A_ID from actors as a, actors as b where (YEAR(a.dob)-YEAR(b.dob)-(DATE_FORMAT(a.dob, '%m%d') < DATE_FORMAT(b.dob, '%m%d')) <= -10));

v)
>select max(dcount), did, df, dl from (select count(movies.MRN) as dcount, directors.D_ID as did, directors.firstname as df, directors.lastname as dl from actors, starred, directors, directed, movies where actors.A_ID = starred.A_ID and directors.D_ID = directed.D_ID and starred.MRN = movies.MRN and directed.MRN = movies.MRN and actors.firstname = "Shahrukh" and actors.lastname = "Khan" group by did) as dfrequency;
'''

mariadb_connection = mariadb.connect(host='localhost', user='public', password='test3R', database='seleri')
additional_connection = mariadb.connect(host='localhost', user='public', password='test3R', database='seleri')
cursor = mariadb_connection.cursor()
backup_cursor = additional_connection.cursor()

try:
	cursor.execute("show tables")

	print("The tables in this database are :")
	for (table_name,) in cursor:
		print("-> {}".format(table_name))
		backup_cursor.execute("select * from %s" % table_name)
		table_contents = backup_cursor.fetchall()
		pprint(table_contents)

	### query 1
	cursor.execute('select title, year from starred, movies where starred.MRN = movies.MRN and starred.A_ID in ( select A_ID from actors where actors.firstname="Shahrukh" and actors.lastname="Khan") ')

	print("\nResult of query no. 1:")
	for title, year in cursor:
		print("movie: {}, released in : {}".format(title, year))

	### query 2
	cursor.execute('select title, year from starred, movies where starred.MRN = movies.MRN and starred.A_ID in (select a.A_ID from actors as a where a.firstname="Shahrukh" and a.lastname="Khan") and movies.MRN in (select directed.MRN from directed, movies where directed.MRN = movies.MRN and directed.D_ID in (select directors.D_ID from directors where directors.firstname="Shahrukh" and directors.lastname="Khan")) ')

	print("\nResult of query no. 2:")
	for title, year in cursor:
		print("movie: {}, released in : {}".format(title, year))

	### query 3
	cursor.execute('select title, year, genre from starred, movies where starred.MRN=movies.MRN and starred.A_ID in (select a.A_ID from actors as a where a.firstname="Shahrukh" and a.lastname="Khan") and movies.genre="thriller" and year>2000 ')

	print("\nResult of query no. 3:")
	for title, year, genre in cursor:
		print("movie: {}, released in: {}, which is a : {}".format(title, year, genre))

	### query 4
	cursor.execute('select distinct actors.firstname, actors.lastname from actors, starred where actors.A_ID=starred.A_ID and starred.MRN in (select starred.MRN from starred, movies where starred.MRN=movies.MRN and starred.A_ID in (select a.A_ID from actors as a where a.firstname="Shahrukh" and a.lastname="Khan")) and starred.A_ID not in (select a.A_ID from actors as a where a.firstname="Shahrukh" and a.lastname="Khan") and actors.A_ID in (select b.A_ID from actors as a, actors as b where (YEAR(a.dob)-YEAR(b.dob)-(DATE_FORMAT(a.dob, "%m%d") < DATE_FORMAT(b.dob, "%m%d")) <= -10)) ')

	print("\nResult of query no. 4:")
	for firstname, lastname in cursor:
		print("actor's name: {} {}".format(firstname, lastname))

	### query 5
	cursor.execute('select max(dcount), did, df, dl from (select count(movies.MRN) as dcount, directors.D_ID as did, directors.firstname as df, directors.lastname as dl from actors, starred, directors, directed, movies where actors.A_ID = starred.A_ID and directors.D_ID = directed.D_ID and starred.MRN = movies.MRN and directed.MRN = movies.MRN and actors.firstname = "Shahrukh" and actors.lastname = "Khan" group by did) as dfrequency ')

	print("\nResult of query no. 5:")
	for max_count, director_id, firstname, lastname in cursor:
		print("max_count: {}, director_id: {}, name:{} {}".format(max_count, director_id, firstname, lastname))

except mariadb.Error as error:
    print("Error: {}".format(error))

#Actually commits the changes to the database
mariadb_connection.commit()
additional_connection.commit()

mariadb_connection.close()
additional_connection.close()