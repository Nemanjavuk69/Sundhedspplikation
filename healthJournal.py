import csv


def get_health_journal(user_id):
    user_id = str(user_id)  # Ensure user_id is a string
    entries = []
    with open('healthJournal.csv', mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['UserID'] == user_id:
                entries.append(row['Entry'])
    return entries
