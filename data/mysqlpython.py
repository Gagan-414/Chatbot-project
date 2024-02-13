#Connect python with PhpMyAdmin and create database (Working)
#
# import mysql.connector
#
# mydb = mysql.connector.connect(
#    host = "localhost",
#    username="root",
#    password = ""
#   )
#
# print(mydb)
#
# mycursor = mydb.cursor()
#
# mycursor.execute("create database chatbot_data_new")
# print("Database created successfully")


# Connection with database created and create table

import pymysql
#database connection
connection = pymysql.connect(host="localhost", user="root", passwd="", database="chatbot_data_new")
cursor = connection.cursor()
# Query for creating table
CreateSqlTable = """CREATE TABLE User_updated(
ID INT(20) PRIMARY KEY AUTO_INCREMENT,
DATE_TIME VARCHAR(250),
NAME  CHAR(25) NOT NULL,
EMAIL CHAR(25),
CONTACT VARCHAR(20),
QUERY VARCHAR(250))"""

cursor.execute(CreateSqlTable)
connection.close()

