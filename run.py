import login
import pymysql
import database

host = "localhost"
user = "root"
password = "" #enter your password
#database = "shopping"
try:
    connection = pymysql.connect(host=host, user=user, password=password)
except pymysql.Error as e:
    print("Error")
    print(e)
else:
    cursor = connection.cursor()
    print("Connection established")
    database.main(connection,cursor)
    login.main(connection,cursor)
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
