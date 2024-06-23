import csv
import os
from constants import CSV_COLUMNS

# Function to read the MVP data CSV file
def read_mvp_data(file_path: str):
    mvp_list = {}
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                mvp_list[row['MVP Code']] = (row['Death Duration Start'], row['Death Duration End'], row['Location'])
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return mvp_list

# Function to read the MVP schedule CSV file
def read_mvp_sched(file_path: str):
    mvp_sched = []
    if not os.path.exists(file_path):
        create_empty_mvp_sched(file_path)
        
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                mvp_sched.append(row)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return mvp_sched

# Function to create an empty MVP schedule CSV file with headers
def create_empty_mvp_sched(file_path: str):
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
            writer.writeheader()
    except Exception as e:
        print(f"Error creating empty CSV file: {e}")

# Function to write to the MVP schedule CSV file
def write_mvp_sched(file_path: str, mvp_sched: list):
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            writer.writerows(mvp_sched)
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
