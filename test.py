import csv


print("HEJ")


# Replace 'example.csv' with the path to your actual CSV file
users = 'users.csv'

with open(users, mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    # Optional: If you want to skip the header
    next(csv_reader, None)

    for row in csv_reader:
        print(row)
