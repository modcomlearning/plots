# Sources of data
#  From a database, Excel, CSV, access, textfiles, doc, pdf
import pandas
# pandas package hhelps a datascientist read data from a source
data = pandas.read_csv('https://modcom.co.ke/datasets/iris.csv')
print(data)
# Step 1: acquire data
# Step 2: Undertand - what is thhe data all about?
print(data.describe())
print(data.dtypes)  # object means string
print(data.corr())
# 0   - No correlation
# from 0 ...1  Positive Correlation  -  when one goes up ,the other goes up
# from 0 ...-1 Negative Correlation - when one goes up, the other come down
print(data.info())
