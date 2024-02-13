from datetime import datetime
import pymysql


def Write_into_SQL(name, email, contact, query):
    # database connection
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="chatbot_data_new")
    from datetime import datetime
    cursor = connection.cursor()
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
    # queries for inserting values
    insert = "INSERT INTO User_updated(DATE_TIME,NAME, EMAIL, CONTACT, QUERY) VALUES (%s, %s, %s, %s, %s)"
    values = (date_time, name, email, contact, query)
    # insert2 = "INSERT INTO Artists(NAME, TRACK) VALUES('Sadduz', 'Rock' );"

    # executing the quires
    cursor.execute(insert, values)
    # cursor.execute(insert2)

    # commiting the connection then closing it.
    connection.commit()
    connection.close()
