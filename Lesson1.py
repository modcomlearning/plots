
import pandas
data = pandas.read_csv("https://modcom.co.ke/datasets/bank.csv")

import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template
plt.style.use('seaborn')
app = Flask(__name__)
@app.route('/')
def plots():
    # plot 1
    sns.distplot(data['LoanAmount'], color='red')
    plt.title('Histogram of  LoanAmount')
    plt.savefig('static/dist.png')

    # plot 2
    sns.boxplot(x='Gender', y='LoanAmount', palette='magma',
                     data=data)
    plt.title('Gender vs LoanAmount')
    plt.savefig('static/box.png')


    return render_template('plots.html')


if __name__ == '__main__':
    app.run()



