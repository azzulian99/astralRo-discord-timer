import csv
from constants import MVP_DATA_FILE, MVP_SCHED_FILE, COORDINATE_BOUNDS, EXCEPTION_CODES

def read_mvp_data(file_path=MVP_DATA_FILE):
    mvp_data = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mvp_data[row['MVP Code']] = (row['Death Duration Start'], row['Death Duration End'], row['Location'])
    return mvp_data

def read_mvp_sched(file_path=MVP_SCHED_FILE):
    mvp_sched = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mvp_sched.append(row)
    return mvp_sched

def write_mvp_sched(file_path, data):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ["MVP Code", "Next Spawn Start", "Next Spawn End", "Location", "Coordinates"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def validate_coordinates(x, y):
    if x is not None and not (0 <= x < COORDINATE_BOUNDS):
        raise ValueError(EXCEPTION_CODES['COORDINATES_OUT_OF_BOUNDS'])
    if y is not None and not (0 <= y < COORDINATE_BOUNDS):
        raise ValueError(EXCEPTION_CODES['COORDINATES_OUT_OF_BOUNDS'])       
