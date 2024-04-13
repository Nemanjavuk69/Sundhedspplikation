import csv
from flask import session


def verify_doctor_credentials(username, password):
    with open('doctors.csv', mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Username'] == username and row['Password'] == password:
                return True, row['Email'], row['ID']
    return False, None, None
