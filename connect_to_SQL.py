import psycopg2

connection = psycopg2.connect(
    database='BackData',
    host='localhost',
    user='postgres',
    password='3008001')

conn = "postgresql://postgres:3008001@localhost/BackData"

