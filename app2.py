import pandas
import pymysql

connection = pymysql.connect(host='localhost', user='root',
                             password='', database='sample_db')

data = pandas.read_sql_query('select * from products', con=connection)
print(data)
print(data.describe())

