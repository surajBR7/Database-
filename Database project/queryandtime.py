import sqlite3
import csv
import time
import json

def load_data_from_csv(file_path, conn):
    """Load data from the CSV file into the database."""
    cursor = conn.cursor()
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['StillWorking'] = 1 if row['StillWorking'].strip().lower() == 'yes' else 0
            cursor.execute('''
                INSERT OR IGNORE INTO employee_data (
                    PersonID, PersonName, SchoolID, SchoolName, SchoolCampus,
                    DepartmentName, DepartmentID, BirthDate, StillWorking,
                    JobID, JobTitle, Earnings, EarningsYear
                ) VALUES (
                    :PersonID, :PersonName, :SchoolID, :SchoolName, :SchoolCampus,
                    :DepartmentName, :DepartmentID, :BirthDate, :StillWorking,
                    :JobID, :JobTitle, :Earnings, :EarningsYear
                )
            ''', row)
    conn.commit()

def run_query(conn, query):
    """Run a SQL query and return the execution time."""
    cursor = conn.cursor()
    start_time = time.time()
    cursor.execute(query)
    cursor.fetchall()  # Execute the query
    end_time = time.time()
    return end_time - start_time

def main():
    queries = [
        "SELECT PersonName FROM employee_data WHERE BirthDate < '1975-01-01' AND Earnings > 130000;",
        "SELECT PersonName, SchoolName FROM employee_data WHERE Earnings > 400000 AND StillWorking = 0;",
        "SELECT PersonName FROM employee_data WHERE SchoolName = 'University of Texas' AND JobTitle = 'Lecturer' AND StillWorking = 0;",
        "SELECT SchoolName, SchoolCampus FROM employee_data WHERE StillWorking = 1 GROUP BY SchoolID ORDER BY COUNT(PersonID) DESC LIMIT 1;",
        "SELECT PersonName, JobTitle, DepartmentName, SchoolName, Earnings FROM employee_data WHERE PersonName = 'Suraj Basavaraj Rajolad';",
        "SELECT DepartmentName FROM employee_data GROUP BY DepartmentName ORDER BY AVG(Earnings) DESC LIMIT 1;"
    ]

    file_sizes = ['./datasets/salary_tracker_1MB.csv', 
                  './datasets/salary_tracker_10MB.csv', 
                  './datasets/salary_tracker_100MB.csv']
    
    execution_times = {query: [] for query in queries}

    # Create SQLite database
    conn = sqlite3.connect('dbproject.db')

    for file_size in file_sizes:
        print(f"\nLoading data from {file_size.split('/')[-1]}...\n")
        load_data_from_csv(file_size, conn)
        
        for query in queries:
            execution_time = run_query(conn, query)
            execution_times[query].append(execution_time)

            # Print the formatted output
            print(f"File: {file_size.split('/')[-1]} | Query: '{query[:30]}...' | Time: {execution_time:.4f} seconds")

    # Save execution times to a JSON file for plotting
    with open('execution_times.json', 'w') as f:
        json.dump(execution_times, f)

    conn.close()

if __name__ == "__main__":
    main()
