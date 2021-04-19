# TODO: Initialize Africa's Talking
import  africastalking
africastalking.initialize(
    username='mwasika',
    api_key='195280c96af1d98ab01d3ed3210e088ef1dbaa24392ef126555566c918a0775d'
)

sms = africastalking.SMS

def sending(phone):
        # TODO: Send message
        recipients = [phone]
        message = 'Thank you for Registering with SOSMAMAS. Remote Monitoring for Mothers'
        sender = 'AFRICASTKNG'  # Place your SenderID here

        try:
            response = sms.send(message, recipients)
            print(response)
        except Exception as e:
            print(f'Houston, something went wrong: ${e}')


def sending_patient(phone, idnumber, fname, rowid):
    # TODO: Send message
    import random
    code = random.randint(1000, 9999)
    print(code)
    recipients = [phone]
    message = "Hi {} You have been registered with SOSMAMAS. Use Patient Id {} and OTP {}".format(fname,rowid, code)
    sender = 'AFRICASTKNG'  # Place your SenderID here
    try:
        response = sms.send(message, recipients)
        print(response)

        import pymysql

        # we first connect to localhost and soko_db
        conn = pymysql.connect(host="localhost", user="root", password="", database="sosmamas")

        # insert the records into the users tables
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO `patient_login`(`patient_id`, `phone`, `code`) VALUES (%s,%s,%s)",
                (rowid, phone, code))
            conn.commit()

        except:
            pass

    except Exception as e:
        print(f'Houston, something went wrong: ${e}')