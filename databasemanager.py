import sqlite3
from MIET_API import *
import datetime

def connectDb():

    filename = "sensors_1.db"

    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    return connection, cursor


def createDatabase():
    connection, cursor = connectDb()
    try:
        cursor.execute("""IF NOT EXISTS (CREATE TABLE data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datetime TEXT,
                    airt1 INTEGER,
                    airt2 INTEGER,
                    airt3 INTEGER,
                    airt4 INTEGER,
                    airh1 INTEGER,
                    airh2 INTEGER,
                    airh3 INTEGER,
                    airh4 INTEGER,
                    gndh1 INTEGER,
                    gndh2 INTEGER,
                    gndh3 INTEGER,
                    gndh4 INTEGER,
                    gndh5 INTEGER,
                    gndh6 INTEGER ))
                """)
    except:
        print('Такая таблица уже существует')

def firstUpdate():
    connection, cursor = connectDb()
    airTableHeadings = ['T1', 'T2', 'T3', 'T4', 'H1', 'H2', 'H3', 'H4']
    AH1, AT1 = RequestAirHT(1)
    AH2, AT2 = RequestAirHT(2)
    AH3, AT3 = RequestAirHT(3)
    AH4, AT4 = RequestAirHT(4)
    airTableData = [[AT1, AT2, AT3, AT4, AH1, AH2, AH3, AH4]]

    groundTableHeadings = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6']
    GH1 = RequestGroundH(1)
    GH2 = RequestGroundH(2)
    GH3 = RequestGroundH(3)
    GH4 = RequestGroundH(4)
    GH5 = RequestGroundH(5)
    GH6 = RequestGroundH(6)
    groundTableData = [[GH1, GH2, GH3, GH4, GH5, GH6]]
    request = f'INSERT INTO data (datetime, airt1, airt2, airt3, airt4, airh1, airh2, airh3, airh4, gndh1, gndh2, gndh3, gndh4, gndh5, gndh6) VALUES ("{datetime.datetime.now()}", {AT1}, {AT2}, {AT3}, {AT4}, {AH1}, {AH2}, {AH3}, {AH4}, {GH1}, {GH2}, {GH3}, {GH4}, {GH5}, {GH6})'
    cursor.execute(request)
    connection.commit()

    return airTableData, airTableHeadings, groundTableData, groundTableHeadings, connection, cursor
