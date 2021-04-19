#  Flask uses HTML/JS/CSS/Python/Jinja2
from flask import Flask, render_template, session, flash, redirect, url_for
from flask import request
import pymysql
from pandas.io import sql

app = Flask(__name__)  # flask object takes the the name of the application
import africastalking
# create a secret key used in encrypting the sessions
app.secret_key = "Wdg@#$%89jMfh2879mT"
# Routing


# functions to hash password
import hashlib, binascii, os
# This function receives a password as a parameter
# its hashes and salts using sha512 encoding
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

@app.route('/Main')
def Main():
    if 'key' in session:
        return render_template('Main.html')
    else:
        return redirect('/')

# this function checks if hashed password is the same as
# provided password
def verify_password(hashed_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = hashed_password[:64]
    hashed_password = hashed_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == hashed_password


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # # hash the password/ strength
        # # we first connect to localhost and soko_db
        conn = pymysql.connect(host = "localhost", user="root", password="", database="sosmamas")

        # insert the records into the users tables
        cursor = conn.cursor()
        cursor.execute("select * from users where email = %s", (email))

        # below we check if there is a match for the email user provided during login
        if cursor.rowcount == 1:
            # take me to a different route and create a session
            rows = cursor.fetchone()
            # get hashed password from db
            hashed_password = rows[7]

            # Provide the hashed password from database and the password user provided
            # check if the are same, if so its true
            status = verify_password(hashed_password, password)
            if status == True:
                # do session here
                # if password are same,  create a session and proceed to patients list route
                session['key'] = email
                from flask import redirect
                # after successful login, we create user session and redirect the user to /Main
                return redirect('/Main')
            else:
                return render_template('login.html', msg="Wrong credentials , Try again")
            # take me to a different route and create a session
        else:
            return render_template('login.html', msg="Email does not exist")

    else:
        return render_template('login.html')




# install python, pycharm, xampp
@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']
        hospital_name = request.form['hospital_name']
        password = request.form['password']
        confirm = request.form['confirm']
        location = request.form['location']
        # confirm not implemented
        # check if confirm password and password are same
        import re
        if password != confirm:
            return render_template('signup.html', msg="Password do not match!")

        # define a code  to check password strength
        elif (len(password) < 8):
            return render_template('signup.html', msg="Must be eight characters")

        elif not re.search("[a-z]", password):
            return render_template('signup.html', msg="Must have at least one small letters")

        elif not re.search("[A-Z]", password):
            return render_template('signup.html', msg="Must have at least one capital letters")


        else:
            # hash the password
            # we first connect to localhost and soko_db
            conn = pymysql.connect(host = "localhost", user="root", password="", database="sosmamas")

            # insert the records into the users tables
            # cursor is used to execute your SQl
            cursor =  conn.cursor()
            try:
                # note the password is hashed in next line at the end
                cursor.execute("INSERT INTO `users`(`fname`, `lname`, `email`, `phone`, `hospital_name`, `location`, `password`) values (%s,%s,%s,%s,%s,%s,%s)", (fname,lname, email, phone, hospital_name,location,hash_password(password)))
                conn.commit() # update the database
                from smss import sending
                sending(phone)
                return render_template('signup.html', msg1="Record Saved Successfully")
            except:
                return render_template('signup.html', msg="Error Occurred During Registration")


    else:
        return render_template('signup.html')




@app.route('/patients', methods=['POST','GET'])
def patients():
    if request.method == "POST":
        phone = request.form['phone']
        # Connect to database
        conn = pymysql.connect(host="localhost", user="root", password="1234D!@#$", database="sosmamas")
        cursor = conn.cursor()
        # execute the query using the cursor
        sql = "select * from patients where phone = %s"
        cursor.execute(sql, (phone))
        # check if no records were found
        if cursor.rowcount < 1:
            flash('Phone number does not exist, try again', 'info')
            return render_template('patients.html')
        else:
            # return all rows found
            # search
            rows = cursor.fetchall()
            return render_template('patients.html', rows=rows)


    else:
        # Connect to database
        conn = pymysql.connect(host="localhost", user="root", password="1234D!@#$", database="sosmamas")
        cursor = conn.cursor()
        # execute the query using the cursor
        cursor.execute("select * from patients")
        # check if no records were found
        if cursor.rowcount < 1:
            return render_template('patients.html', msg="No Patients, Please add patients")
        else:
            # return all rows found
            # search
            rows = cursor.fetchall()

            return render_template('patients.html', rows=rows)







# install python, pycharm, xampp
@app.route('/add', methods=['POST','GET'])
def add():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']
        id_number = request.form['id_number']
        next_of_kin_name = request.form['next_of_kin_name']
        next_of_kin_phone = request.form['next_of_kin_phone']
        residence = request.form['residence']
        dob = request.form['dob']


        # hash the password
        # we first connect to localhost and soko_db
        conn = pymysql.connect(host = "localhost", user="root", password="", database="sosmamas")

        # insert the records into the users tables
        cursor =  conn.cursor()
        try:
            cursor.execute("INSERT INTO `patients`(`id_number`, `fname`, `lname`, `email`, `phone`,`next_of_kin_name`, `next_of_kin_phone`, `dob`, `residence`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (id_number,fname,lname, email, phone, next_of_kin_name, next_of_kin_phone, dob, residence))
            conn.commit()
            from smss import sending_patient
            rowid = cursor.lastrowid
            print(rowid)
            sending_patient(phone, id_number, fname, rowid)
            flash('Record Saved Successfully','success')
            return redirect(url_for('patients'))

        except:
            flash('Error Occurred During Registration, Id/Phone Already used','danger')
            return redirect(url_for('patients'))


    else:
        return redirect('/patients')




# install python, pycharm, xampp
# provide the patient id to update
    # provide the patient id to retrieve the patient record
@app.route('/retrieve_patient_to_update/<patient_id>', methods=['POST', 'GET'])
def retrieve_patient_to_update(patient_id):
        # first we fetch the details of the patient
        conn = pymysql.connect(host="localhost", user="root", password="", database="sosmamas")
        cursor = conn.cursor()
        sql = 'Select * from patients where patient_id = %s'
        cursor.execute(sql, (patient_id))

        if cursor.rowcount == 0:
            flash('No Records ', 'danger')
            return redirect(url_for('patients'))
        else:
            row = cursor.fetchone()
            # return the records to patient_update.html  and place the fields in the form for doctor to change
            return render_template('patient_update.html', row=row)


# this is the route to make the update once the doctor clicks the update button on patient updat eform
@app.route('/update_patient', methods=['POST', 'GET'])
def update_patient():
    if request.method == "POST":
        patient_id = request.form['patient_id']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']
        next_of_kin_name = request.form['next_of_kin_name']
        next_of_kin_phone = request.form['next_of_kin_phone']
        residence = request.form['residence']

        # hash the password
        # we first connect to localhost and soko_db
        conn = pymysql.connect(host="localhost", user="root", password="", database="sosmamas")

        # insert the records into the users tables
        cursor = conn.cursor()
        try:
            sql = "UPDATE `patients`  SET `fname` = %s,  `lname` = %s,  `email` = %s, `phone` = %s, " \
                  "`next_of_kin_name`=%s, `next_of_kin_phone`=%s,`residence`= %s  where patient_id = %s "
            cursor.execute(sql,
                           (fname, lname, email, phone, next_of_kin_name, next_of_kin_phone, residence, patient_id))
            conn.commit()
            flash('Update Successfully', 'success')
            return redirect(url_for('patients'))

        except:
            flash('Update Failed, Try Again', 'danger')
            return redirect(url_for('patients'))
    else:
        flash('Please the edit icon to update patient record', 'info')
        return redirect(url_for('patients'))



@app.route('/test/<patient_id>')
def test(patient_id):
    return render_template('add_test.html', patient_id = patient_id)

# install python, pycharm, xampp
@app.route('/add_test', methods=['POST','GET'])
def add_test():
    if request.method == "POST":
        patient_id = request.form['patient_id']
        weight = request.form['weight']
        height = request.form['height']
        heart_rate = request.form['heart_rate']
        temparature = request.form['temparature']
        systolic = request.form['systolic']
        diastolic = request.form['diastolic']
        # hash the password
        # we first connect to localhost and soko_db
        conn = pymysql.connect(host = "localhost", user="root", password="1234D!@#$", database="sosmamas")

        # insert the records into the users tables
        cursor =  conn.cursor()
        try:
            cursor.execute("INSERT INTO `tests`(`patient_id`, `weight`, `height`, `heart_rate`, `temperature`, `systolic`, `diastolic`) values (%s,%s,%s,%s,%s,%s,%s)", (patient_id,weight,height, heart_rate, temparature, systolic, diastolic))
            conn.commit()
            flash('Record Saved Successfully','success')
            return redirect(url_for('patients'))

        except:
            flash('Error Occurred During Recording','danger')
            return redirect(url_for('patients'))


    else:
        return render_template('')



import matplotlib.pyplot as plt
@app.route('/records/<id>')
def records(id):
    if id == "":
        return redirect('/patients')
    # Connect to database
    else:

        conn = pymysql.connect(host="localhost", user="root", password="1234D!@#$", database="sosmamas")
        sql11 = "select * from weeks  where patient_id =%s"
        cursor = conn.cursor()
        cursor.execute(sql11, (id))
        if cursor.rowcount ==0:
            total_weeks = 0
        else:
            row1 = cursor.fetchone()
            weeks = row1[2]
            old_date = row1[3]

            # NOTE: example using Python 3.x
            import datetime
            # Prior date example of "11 July 2013"
            # old_date = datetime.date(date)
            old_date2 = old_date.date()


            # New date example of "today"
            new_date = datetime.date.today()
            print(type(old_date2))
            date_delta = new_date - old_date2
            # date_delta is a "datetime.timedelta" object
            # "date_delta.days" gives an integer number of days
            no_of_weeks = date_delta.days / 7.0
            import  math
            no_of_weeks = math.trunc(no_of_weeks)
            total_weeks = int(no_of_weeks) + int(weeks)


        # use patient id to the
        cursor = conn.cursor()
        sql = "Select * from patients where patient_id = %s"
        cursor.execute(sql, (id))
        row_details = cursor.fetchone()


        global patient_id

        sql = 'Select * from tests where patient_id = %s'
        cursor.execute(sql, (id))

        if cursor.rowcount == 0:
            flash('No Records for this patient, click on test button to record patients tests ','warning')
            return redirect(url_for('patients'))

        else:
            # cursor.execute("select * from tests")



            plt.style.use('ggplot')
            import  seaborn
            import pandas
            data = pandas.read_sql("select * from tests where patient_id = %(id)s", conn, parse_dates=['created_date'], params={"id":id})
            print(data)
            data['weight'] = data['weight'].astype(float)
            # data['height'] = data['height'].astype(float)
            data['temperature'] = data['temperature'].astype(float)
            data['heart_rate'] = data['heart_rate'].astype(float)
            data['systolic'] = data['systolic'].astype(float)
            data['diastolic'] = data['diastolic'].astype(float)


            patterns = data[['temperature', 'created_date']]
            patterns = patterns.set_index('created_date')
            patterns.resample('M').mean().plot(title='Temperature by day')
            plt.xlabel("Date in days")
            plt.ylabel("Temparature in Degrees")
            plt.savefig("static/temp.png")


            patterns = data[['weight', 'created_date']]
            patterns = patterns.set_index('created_date')
            patterns.resample('M').mean().plot(title='Weight By Day', legend=True)
            plt.xlabel("Date in Days")
            plt.ylabel("Weight - Kgs")
            plt.savefig("static/weight.png")


            patterns = data[['heart_rate', 'created_date']]
            patterns = patterns.set_index('created_date')
            patterns.resample('M').mean().plot(title='Heart Rate By Day', legend=True)
            plt.xlabel("Date - Days")
            plt.ylabel("heart_rate - lb")
            plt.savefig("static/heart.png")


            patterns = data[['systolic', 'diastolic', 'created_date']]
            patterns = patterns.set_index('created_date')
            patterns.resample('M').mean().plot(title='Blood Pressure', xlabel= 'Date' , legend=True)
            plt.xlabel("Date")
            plt.ylabel("Blood Presure - lb")
            plt.savefig("static/pressure.png")


            rows = cursor.fetchall()
            for row in rows:
                patient_id = row[1]


            return render_template('records.html', rows = rows, row_details = row_details, patient_id = patient_id, weeks= total_weeks)
    # # execute the query using the cursor


# view prescription by patient,
@app.route('/prescription/<patient_id>')
def prescription(patient_id):
    # Connect to database
    conn = pymysql.connect(host = "localhost", user="root", password="1234D!@#$", database="sosmamas")
    cursor = conn.cursor()

    sql1 = "select * from patients  where patient_id =%s"
    cursor.execute(sql1, (patient_id))
    row = cursor.fetchone()
    phone = row[5]
    print(phone)


    # execute the query using the cursor
    sql = "select * from prescription  where patient_id = %s order by date_created desc"
    cursor.execute(sql, (patient_id))
    # check if no records were found
    if cursor.rowcount < 1:
        flash('No prescription for this patient', 'danger')
        #print('No records')
        return render_template('prescription.html', patient_id = patient_id, token=1)
    else:
        #return all rows found
        #Search
        import pandas
        data = pandas.read_sql("select * from prescription where patient_id = %(id)s ", conn, parse_dates=['date_created'],
                               params={"id": patient_id})
        print('here', data)
        import matplotlib.pyplot as plt
        if data.empty:
            print('DataFrame is empty!')

        plt.style.use('ggplot')

        x, y = plt.subplots()
        data.groupby("medicine").size().plot(kind='pie', title= 'Proportion of Medicine Given in %', autopct = '%1.1f%%')
        plt.xlabel("")
        plt.ylabel("")
        plt.savefig("static/pie.png")


        x, y = plt.subplots()
        plt.ylim(0, 10)
        data.groupby("medicine")['medicine'].count().plot(kind='bar', title='Medicine by Times Given')
        plt.xlabel("Medicine Name")
        plt.ylabel("Number of times given")
        plt.savefig("static/bar.png")

        from matplotlib import rcParams
        rcParams.update({'figure.autolayout': True})


        x, y = plt.subplots()
        data = pandas.read_sql("select * from prescription where patient_id = %(id)s ", conn, parse_dates=['date_created'],
                               params={"id": patient_id})

        data['date_created'] = pandas.to_datetime(data['date_created']).dt.date

        data = data.groupby(["date_created", "medicine"]).size().unstack()

        data.plot(kind='bar', title='Doses Given by Date')
        plt.xlabel("Date Prescribed")
        plt.ylabel("Doses Given")
        plt.title("Doses Given by Date")
        plt.legend(bbox_to_anchor=(1.1, 1.05))
        plt.savefig("static/bar_drugs.png")

        flash('Below are Patient Prescriptions', 'info')
        rows = cursor.fetchall()
        return render_template('prescription.html',rows=rows, patient_id = patient_id, phone=phone)




# install python, pycharm, xampp
@app.route('/add_prescription', methods=['POST','GET'])
def add_prescription():
    if request.method == "POST":
        patient_id = request.form['patient_id']
        prescription_name = request.form['prescription_name']
        dosage = request.form['dosage']
        duration = request.form['duration']


        # hash the password
        # we first connect to localhost and soko_db
        conn = pymysql.connect(host = "localhost", user="root", password="", database="sosmamas")
        # insert the records into the users tables
        cursor =  conn.cursor()
        try:
            cursor.execute("INSERT INTO `prescription`(`patient_id`, `medicine`, `dosage`, `duration`) values (%s,%s,%s,%s)", (patient_id, prescription_name, dosage, duration))
            conn.commit()
            flash('Prescription Saved Successfully','success')
            return redirect(url_for('prescription', patient_id = patient_id))

        except:
            flash('Error Occurred During Recording', 'danger')
            return redirect(url_for('patients', patient_id = patient_id))

    else:
        return render_template('')



# get prescription by prescription_id
@app.route('/view_prescription_to_edit/<prescription_id>/<patient_id>')
def view_prescription_to_edit(prescription_id, patient_id):
    # first we fetch the details of the patient
    conn = pymysql.connect(host="localhost", user="root", password="", database="sosmamas")
    cursor = conn.cursor()
    sql = 'Select * from prescription where prescription_id = %s'
    cursor.execute(sql, (prescription_id))

    if cursor.rowcount == 0:
        flash('Click on Records Button to get patients records', 'danger')
        return redirect(url_for('patients'))
    else:
        row = cursor.fetchone()
        # return the records to prescription_update.html  and place the fields in the form for doctor to change
        return render_template('prescription_update.html', row=row, patient_id=patient_id)



# this is the route to make the update once the doctor clicks the update button on patient updat eform
@app.route('/update_prescription', methods=['POST', 'GET'])
def update_prescription():
    if request.method == "POST":
        patient_idd = request.form['patient_id']
        prescription_id = request.form['prescription_id']
        prescription_name = request.form['prescription_name']
        dosage = request.form['dosage']
        duration = request.form['duration']

        # hash the password
        # we first connect to localhost and soko_db
        conn = pymysql.connect(host="localhost", user="root", password="", database="sosmamas")

        # insert the records into the users tables
        cursor = conn.cursor()
        try:
            sql = "UPDATE `prescription`  SET `medicine` = %s,  `dosage` = %s,  `duration` = %s  where " \
                  "prescription_id = %s "
            cursor.execute(sql,
                           (prescription_name, dosage, duration,prescription_id))
            conn.commit()
            flash('Prescription Updated Successfully', 'success')
            return redirect(url_for('prescription', patient_id=patient_idd))

        except:
            flash('Update Failed, Try Again', 'danger')
            return redirect(url_for('prescription', patient_id=patient_idd))
    else:
        flash('Please the edit icon to update patient record', 'info')
        return redirect(url_for('patients'))




@app.route('/alert/<patient_phone>')
def alert(patient_phone):
    import africastalking
    africastalking.initialize(
        username='mwasika',
        api_key='195280c96af1d98ab01d3ed3210e088ef1dbaa24392ef126555566c918a0775d'
    )
    sms = africastalking.SMS
    recipients = [patient_phone]
    message = 'You have a prescription from the doctor, check SOSMAMAS app, Thank you.'
    sender = 'AFRICASTKNG'  # Place your SenderID here

    try:
        response = sms.send(message, recipients)
        print(response)
    except Exception as e:
        print(f'Houston, something went wrong: ${e}')

    return redirect('/patients')


@app.route('/logout')
def logout():
    session.pop('key',None)
    from flask import redirect
    return redirect('/')



# install python, pycharm, xampp
@app.route('/weeks', methods=['POST','GET'])
def weeks():
    if request.method == "POST":
        patient_id = request.form['patient_id']
        weeks = request.form['weeks']

        # hash the password
        # we first connect to localhost and soko_db
        conn = pymysql.connect(host = "localhost", user="root", password="", database="sosmamas")

        # insert the records into the users tables
        cursor =  conn.cursor()
        try:
            cursor.execute("INSERT INTO `weeks`(`patient_id`, `weeks`) values (%s,%s)", (patient_id,weeks))
            conn.commit()
            flash('Record Saved Successfully','success')
            return redirect(url_for('patients'))

        except:
            flash('Error Occurred During Recording','danger')
            return redirect(url_for('patients'))


    else:
        return render_template('add_test.html')



# Install python, pycharm, xampp
@app.route('/change', methods=['POST','GET'])
def change():
    if 'key' in session:
        email = session['key']
        conn = pymysql.connect(host="localhost", user="root", password="", database="sosmamas")
        cursor = conn.cursor()
        sql = 'Select * from users where email = %s'
        cursor.execute(sql, (email))
        row = cursor.fetchone()
        return render_template('change.html', row = row)
    else:
        return redirect('/login')




# this is the route to make the update once the doctor clicks the update button on patient updat eform
@app.route('/update_details', methods=['POST', 'GET'])
def update_details():
    if 'key' in session:
        email = session['key']
        if request.method == "POST":
            phone = request.form['phone']
            # hash the password
            # we first connect to localhost and soko_db
            conn = pymysql.connect(host="localhost", user="root", password="", database="sosmamas")

            # insert the records into the users tables
            cursor = conn.cursor()
            try:
                sql = "UPDATE `users`  SET `phone` = %s  where " \
                      "email = %s "
                cursor.execute(sql,
                               (phone, email))
                conn.commit()
                flash('Contact Updated Successfully', 'success')
                return redirect(url_for('patients'))

            except:
                flash('Update Failed, Try Again', 'danger')
                return redirect(url_for('patients'))
        else:
            flash('Update Failed, Try Again', 'info')
            return redirect(url_for('patients'))

    else:
        return redirect('/login')



# Install python, pycharm, xampp
@app.route('/view_profile')
def view_profile():
    if 'key' in session:
        email = session['key']
        conn = pymysql.connect(host="localhost", user="root", password="", database="sosmamas")
        cursor = conn.cursor()
        sql = 'Select * from users where email = %s'
        cursor.execute(sql, (email))
        row = cursor.fetchone()
        return render_template('profile.html', row = row)
    else:
        return redirect('/login')



from datetime import date
import datetime


def from_dob_to_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))



@app.route("/general_stats")
def general_stats():
    conn = pymysql.connect(host="localhost", user="root", password="1234D!@#$", database="sosmamas")
    import pandas

    from matplotlib import rcParams
    rcParams.update({'figure.autolayout': True})
    data = pandas.read_sql("select * from patients ", conn, parse_dates=['date_created'])
    plt.style.use('ggplot')

    x, y = plt.subplots()
    data.groupby("county").size().plot(kind='bar', title='Distribution of Patient By County')
    plt.xlabel("")
    plt.ylabel("")
    plt.savefig("static/pie_county.png")


    data['dob'] = pandas.to_datetime(data['dob'])


    data['dob']= data['dob'].apply(lambda x: from_dob_to_age(x))
    print(data['dob'])
    print(data)
    x, y = plt.subplots()
    data.groupby("county")['dob'].mean().plot(kind='bar', title='Average Age By County')
    plt.xlabel("County")
    plt.ylabel("Average Age - Yrs")
    plt.savefig("static/bar_age.png")

    from matplotlib import rcParams
    rcParams.update({'figure.autolayout': True})
    import seaborn as sns
    x, y = plt.subplots()
    xx = sns.distplot(data['dob'], color='red', kde = False)
    plt.title('Overall Distribution of Age in Yrs')
    plt.xlabel("Age - Yrs")
    plt.ylabel("Freq")
    x.savefig('static/dist_age.png')


    data2 = pandas.read_sql("select * from tests ", conn, parse_dates=['date_created'])
    # # data['dob'] = pandas.to_datetime(data['dob'])
    from matplotlib import rcParams
    rcParams.update({'figure.autolayout': True})
    import seaborn as sns

    x, y = plt.subplots()
    xx = sns.distplot(data2['temperature'], color='red', kde = False)
    plt.title('Overall Distribution of Temperature')
    plt.xlabel("Temp - C")
    plt.ylabel("Freq")
    x.savefig('static/temp.png')
    # #

    x, y = plt.subplots()
    sns.distplot(data2['weight'], color='blue', kde = False)
    plt.title('Distribution of Weight')
    plt.xlabel("Weight - Kgs")
    plt.ylabel("Freq")
    x.savefig('static/weight.png')
    # #

    x, y = plt.subplots()
    sns.distplot(data2['heart_rate'], color='blue', kde=False)
    plt.title('Overall Distribution of Heart Rate')
    plt.xlabel("Heart Rate - BPM")
    plt.ylabel("Freq")
    x.savefig('static/rate.png')


    import seaborn as sns
    data1 = pandas.read_sql("SELECT patients.patient_id, patients.fname, patients.county, patients.dob, tests.weight, tests.temperature, tests.systolic, tests.diastolic FROM patients INNER JOIN tests ON patients.patient_id=tests.patient_id WHERE tests.systolic > 130 and tests.systolic <=139 or tests.diastolic > 80 and tests.diastolic <=89 GROUP by patients.patient_id", conn)
    # data1['weight'] = data1['weight'].astype(float)
    # data1['temperature'] = data1['temperature'].astype(float)
    data1['systolic'] = data1['systolic'].astype(float)
    data1['diastolic'] = data1['diastolic'].astype(float)
    x, y = plt.subplots()
    data1.groupby("county").size().plot(kind='bar', title='Hypertension Stage 1 By Counties'
    )
    plt.xlabel("")
    plt.ylabel("")
    plt.savefig("static/hyper_county_stg1.png")

    data2 = pandas.read_sql(
    "SELECT patients.patient_id, patients.fname, patients.county, patients.dob, tests.weight, tests.temperature, tests.systolic, tests.diastolic FROM patients INNER JOIN tests ON patients.patient_id=tests.patient_id WHERE tests.systolic > 140 and tests.systolic <=180 or tests.diastolic > 90 and tests.diastolic <=120 GROUP by patients.patient_id",
    conn)
    # data1['weight'] = data1['weight'].astype(float)
    # data1['temperature'] = data1['temperature'].astype(float)
    data2['systolic'] = data2['systolic'].astype(float)
    data2['diastolic'] = data2['diastolic'].astype(float)
    x, y = plt.subplots()
    data2.groupby("county").size().plot(kind='bar', title='Hypertension Stage 2 by Counties'
    )
    plt.xlabel("")
    plt.ylabel("")
    plt.savefig("static/hyper_county_stg2.png")


    data3 = pandas.read_sql(
    "SELECT patients.patient_id, patients.fname, patients.county, patients.dob, tests.weight, tests.temperature, tests.systolic, tests.diastolic FROM patients INNER JOIN tests ON patients.patient_id=tests.patient_id WHERE tests.systolic > 180 or tests.diastolic > 120 GROUP by patients.patient_id",
    conn)
    # data1['weight'] = data1['weight'].astype(float)
    # data1['temperature'] = data1['temperature'].astype(float)
    data3['systolic'] = data3['systolic'].astype(float)
    data3['diastolic'] = data3['diastolic'].astype(float)
    x, y = plt.subplots()
    data3.groupby("county").size().plot(kind='bar', title='Hypertensive Crisis by Counties'
    )
    plt.xlabel("")
    plt.ylabel("")
    plt.savefig("static/hyper_county_crisis.png")

    data4 = pandas.read_sql(
    "SELECT patients.patient_id, patients.fname, patients.county, patients.dob, tests.weight, tests.temperature, tests.systolic, tests.diastolic FROM patients INNER JOIN tests ON patients.patient_id=tests.patient_id WHERE tests.systolic < 120 and tests.diastolic < 80 GROUP by patients.patient_id",
    conn)
    # data1['weight'] = data1['weight'].astype(float)
    # data1['temperature'] = data1['temperature'].astype(float)
    data4['systolic'] = data4['systolic'].astype(float)
    data4['diastolic'] = data4['diastolic'].astype(float)
    x, y = plt.subplots()
    data4.groupby("county").size().plot(kind='bar', title='Normal Blood Pressure by Counties'
    )
    plt.xlabel("")
    plt.ylabel("")
    plt.savefig("static/hyper_county_normal.png")

    data5 = pandas.read_sql(
    "SELECT patients.patient_id, patients.fname, patients.county, patients.dob, tests.weight, tests.temperature, tests.systolic, tests.diastolic FROM patients INNER JOIN tests ON patients.patient_id=tests.patient_id WHERE tests.systolic > 140 and tests.systolic <=180 or tests.diastolic > 90 and tests.diastolic <=120 GROUP by patients.patient_id",
    conn)
    # data1['weight'] = data1['weight'].astype(float)
    # data1['temperature'] = data1['temperature'].astype(float)
    data5['systolic'] = data5['systolic'].astype(float)
    data5['diastolic'] = data5['diastolic'].astype(float)

    data5['dob'] = pandas.to_datetime(data5['dob'])
    data5['dob'] = data5['dob'].apply(lambda x: from_dob_to_age(x))

    print(data5['dob'])

    x, y = plt.subplots()
    xx = sns.distplot(data5['dob'], color='red', kde = False)
    plt.title('Age affected by Hypertensive Stage 1')
    plt.xlabel("Age - Yrs")
    plt.ylabel("Freq")
    x.savefig('static/age_affected_st1.png')

    data6 = pandas.read_sql(
    "SELECT patients.patient_id, patients.fname, patients.county, patients.dob, tests.weight, tests.temperature, tests.systolic, tests.diastolic FROM patients INNER JOIN tests ON patients.patient_id=tests.patient_id WHERE tests.systolic > 130 and tests.systolic <=139 or tests.diastolic > 80 and tests.diastolic <=89 GROUP by patients.patient_id",
    conn)
    # data1['weight'] = data1['weight'].astype(float)
    # data1['temperature'] = data1['temperature'].astype(float)
    data6['systolic'] = data6['systolic'].astype(float)
    data6['diastolic'] = data6['diastolic'].astype(float)

    data6['dob'] = pandas.to_datetime(data6['dob'])
    data6['dob'] = data6['dob'].apply(lambda x: from_dob_to_age(x))

    print(data6['dob'])

    x, y = plt.subplots()
    xx = sns.distplot(data6['dob'], color='red', kde=False)
    plt.title('Age affected by Hypertensive Stage 2')
    plt.xlabel("Age - Yrs")
    plt.ylabel("Freq")
    x.savefig('static/age_affected_st2.png')

    data = pandas.read_sql(
        "SELECT medicine, COUNT(medicine) As num FROM `prescription` GROUP bY medicine order by num desc limit 5", conn)
    print(data)

    x, y = plt.subplots()
    data.groupby("medicine")['num'].mean().plot(kind='bar', title='Five Most Common Medicine Given in %')
    plt.xlabel("Medicine")
    plt.ylabel("Count")
    plt.savefig("static/bar_most_common.png")


    data8 = pandas.read_sql(
        "SELECT medicine, COUNT(medicine) As num FROM `prescription` GROUP bY medicine order by num asc limit 5", conn)
    x, y = plt.subplots()
    data8.groupby("medicine")['num'].mean().plot(kind='bar', title='Five Least Common Medicine Given', color='orange')
    plt.xlabel("Medicine")
    plt.ylabel("Count")
    plt.savefig("static/bar_least_common.png")

    cursor = conn.cursor()
    cursor.execute("select * from patients")
    count1 = cursor.rowcount

    cursor.execute(
        "select * from tests WHERE systolic > 140 and systolic <=180 or diastolic > 90 and diastolic <=120 GROUP by patient_id")
    count2 = cursor.rowcount


    percent1 = round(count2/count1 * 100, 2)

    #--------

    cursor.execute(
        "select * from tests WHERE systolic > 130 and systolic <=139 or diastolic > 80 and diastolic <=89 GROUP by patient_id")
    count3 = cursor.rowcount

    percent2 = round(count3 / count1 * 100, 2)


    cursor.execute(
        "select * from tests WHERE systolic > 180 or diastolic > 120 GROUP by patient_id")
    count4 = cursor.rowcount

    percent4 = round(count4 / count1 * 100, 2)


    cursor.execute(
        "select * from tests WHERE systolic < 120 and diastolic < 80  GROUP by patient_id")
    count5 = cursor.rowcount

    percent5 = round(count5 / count1 * 100, 2)


    return render_template('general_stats.html', stage1 = percent1, stage2 = percent2, crisis = percent4, normal = percent5)



@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response



if __name__ == '__main__':
    app.debug = True
    app.run()