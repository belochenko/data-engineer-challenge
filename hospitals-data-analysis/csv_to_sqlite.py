import sqlite3
import csv

csv_file_path = 'data/hospital_trials.csv'

# Connect to an SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('../hospital_data.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS trial_data (
    trial_code TEXT,
    hospital_id TEXT
)
''')

# Open the CSV file and insert each row into the SQLite table
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    # Skip the header
    next(csv_reader)
    # Prepare a list to collect rows
    rows_to_insert = []
    for row in csv_reader:
        # Add a tuple with the values for each row to the list
        rows_to_insert.append(tuple(row))

    # Just memory-optimization part
        # If we have a batch of 500, insert them and clear the list
        if len(rows_to_insert) == 500:
            cursor.executemany('INSERT INTO trial_data (trial_code, hospital_id) VALUES (?, ?)', rows_to_insert)
            conn.commit()
            rows_to_insert = []

    # Insert any remaining rows
    if rows_to_insert:
        cursor.executemany('INSERT INTO trial_data (trial_code, hospital_id) VALUES (?, ?)', rows_to_insert)
        conn.commit()

# Close the connection
conn.close()
