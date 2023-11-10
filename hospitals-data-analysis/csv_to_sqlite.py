import sqlite3
import csv
from itertools import islice, chain


def grouper(iterable, n):
    """Collect data into fixed-length chunks or blocks"""
    # islice() allows to slice the generator
    iterator = iter(iterable)
    for first in iterator:  # stops when iterator is depleted
        yield tuple(islice(chain([first], iterator), n - 1))


def import_csv_to_sqlite(db_path, csv_file_path, batch_size=500):
    # Connect to the SQLite database using a context manager
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Create the trial_data table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trial_data (
                trial_code TEXT,
                hospital_id TEXT
            )
        ''')

        try:
            # Open the CSV file using a context manager
            with open(csv_file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                next(csv_reader)  # Skip the header row

                # Use the grouper function to insert in batches
                for batch in grouper(csv_reader, batch_size):
                    cursor.executemany('INSERT INTO trial_data (trial_code, hospital_id) VALUES (?, ?)', batch)

                conn.commit()  # Commit the transaction
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error: {e}")


# Define paths and call the function
database_path = '../hospital_data.db'
csv_file_path = 'data/hospital_trials.csv'

import_csv_to_sqlite(database_path, csv_file_path)
