import csv
from datetime import datetime, timedelta
import pytz

ph_tz = pytz.timezone('Asia/Manila')

import re
from random import randint, choice
import logging
from constants import MVP_DATA_FILE, MVP_SCHED_FILE, EXCEPTION_CODES
from fileUtils import read_mvp_data, read_mvp_sched, write_mvp_sched, validate_coordinates

logger = logging.getLogger(__name__)

now = datetime.now(ph_tz)
today_date = now.date()

def parse_add_command(user_input: str, mvp_data: dict):
    try:
        code, death_time, x, y, optional_int = extract_command_parts(user_input, mvp_data)
        if code not in ['LHZ3', 'LHZ4', 'THANA']:
            validate_coordinates(x, y)
        death_time = parse_death_time(death_time)
        return (code, death_time, x, y, optional_int), None
    except ValueError as e:
        logger.error("Error parsing command: %s", str(e))
        return None, str(e)

def extract_command_parts(user_input: str, mvp_data: dict):
    pattern = r'-mvp add (\w+)\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*(\d{1,3})?\s*(\d{1,3})?(?:\s+(\d+))?'
    match = re.match(pattern, user_input)
    if not match:
        raise ValueError(EXCEPTION_CODES['INVALID_FORMAT'])
    code, death_time, x, y, optional_int = match.groups()
    if code not in mvp_data:
        raise ValueError(EXCEPTION_CODES['INVALID_MVP_CODE'])
    x = int(x) if x else None
    y = int(y) if y else None
    optional_int = int(optional_int) if optional_int else None
    return code, death_time, x, y, optional_int


def parse_death_time(death_time: str):
    try:
        if len(death_time) == 5:  # h:mm format
            return now.strptime(death_time, '%H:%M')
        elif len(death_time) == 7:  # h:mm:ss format
            return now.strptime(death_time, '%H:%M:%S')
        elif len(death_time) == 8:  # hh:mm:ss format
            return now.strptime(death_time, '%H:%M:%S')
        elif len(death_time) == 4:  # hh:mm format
            return now.strptime(death_time, '%H:%M')
        else:
            raise ValueError()
    except ValueError:
        raise ValueError(EXCEPTION_CODES['INVALID_TIME_FORMAT'])

def add_or_update_mvp_sched(parsed_data, mvp_data, mvp_sched_file):
    try:
        new_entry = create_new_entry(parsed_data, mvp_data)
        mvp_sched = read_mvp_sched(mvp_sched_file)
        update_or_add_entry(mvp_sched, new_entry)
        write_mvp_sched(mvp_sched_file, mvp_sched)
        return format_sched_for_display(mvp_sched)
    except Exception as e:
        logger.exception("Error adding or updating MVP schedule")
        return f"An error occurred: {str(e)}"

def create_new_entry(parsed_data, mvp_data):
    code, death_time, x, y, _ = parsed_data
    death_duration_start, death_duration_end, location = get_death_durations_and_location(mvp_data, code)
    next_spawn_start, next_spawn_end = calculate_next_spawns(death_time, death_duration_start, death_duration_end)
    return {
        'MVP Code': code,
        'Next Spawn Start': next_spawn_start.strftime('%Y-%m-%d %H:%M:%S'),
        'Next Spawn End': next_spawn_end.strftime('%Y-%m-%d %H:%M:%S'),
        'Location': location,
        'Coordinates': f"{x} {y}" if x is not None and y is not None else ""
    }

def get_death_durations_and_location(mvp_data, code):
    death_duration_start_str, death_duration_end_str, location = mvp_data[code]
    death_duration_start = timedelta(hours=int(death_duration_start_str.split(':')[0]), minutes=int(death_duration_start_str.split(':')[1]))
    death_duration_end = timedelta(hours=int(death_duration_end_str.split(':')[0]), minutes=int(death_duration_end_str.split(':')[1]))
    return death_duration_start, death_duration_end, location

def calculate_next_spawns(death_time, death_duration_start, death_duration_end):
    
    next_spawn_start = now.combine(today_date, death_time.time()) + death_duration_start
    next_spawn_end = now.combine(today_date, death_time.time()) + death_duration_end
    return next_spawn_start, next_spawn_end

def update_or_add_entry(mvp_sched, new_entry):
    for entry in mvp_sched:
        if entry['MVP Code'] == new_entry['MVP Code']:
            entry.update(new_entry)
            return
    mvp_sched.append(new_entry)

def format_data_for_display(mvp_data):
    try:
        formatted_data = "\n".join(
            [f"{code} | {start} | {end} | {location}" for code, (start, end, location) in mvp_data.items()]
        )
        return f"```\nMVP Data:\nMVP Code | Death Duration Start | Death Duration End | Location\n{'-' * 65}\n{formatted_data}\n```"
    except Exception as e:
        logger.exception("Error formatting MVP data for display")
        return f"An error occurred: {str(e)}"

def format_sched_for_display(mvp_sched):
    try:
        if not mvp_sched:
            return "MVP schedule is empty."
        mvp_sched.sort(key=lambda x: now.strptime(x['Next Spawn Start'], '%Y-%m-%d %H:%M:%S'))
        current_date = now.strftime("%b/%d/%Y")
        formatted_sched = f"MVP Schedule for {current_date} (Current Time: {now.strftime('%I:%M:%S %p')}):\n"

        formatted_sched += "\n".join(
            [format_sched_row(index, row) for index, row in enumerate(mvp_sched)]
        )
        return f"```\n{formatted_sched}\n```"
    except Exception as e:
        logger.exception("Error formatting MVP schedule for display")
        return f"An error occurred: {str(e)}"

def format_sched_row(index, row):
    current_datetime = now;
    location_and_coords = f"{row['Location']} {row['Coordinates']}".strip()
    next_spawn_start = now.strptime(row['Next Spawn Start'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)
    next_spawn_start_formatted = next_spawn_start.strftime('%I:%M:%S %p')
    remarks = 'NEXT DAY' if next_spawn_start.date() > current_datetime.date() else 'EXPIRED' if current_datetime > next_spawn_start else ''
    return f"{index + 1}: {row['MVP Code']} | {next_spawn_start_formatted} | {location_and_coords} | {remarks}"

def delete_from_mvp_sched(index, mvp_sched_file):
    try:
        mvp_sched = read_mvp_sched(mvp_sched_file)
        if index < 1 or index > len(mvp_sched):
            return EXCEPTION_CODES['INVALID_INDEX']
        del mvp_sched[index - 1]
        write_mvp_sched(mvp_sched_file, mvp_sched)
        return format_sched_for_display(mvp_sched)
    except Exception as e:
        logger.exception("Error deleting entry from MVP schedule")
        return f"An error occurred: {str(e)}"

def clear_mvp_sched(mvp_sched_file):
    try:
        with open(mvp_sched_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["MVP Code", "Next Spawn Start", "Next Spawn End", "Location", "Coordinates"])
            writer.writeheader()
        return "All entries cleared successfully."
    except Exception as e:
        logger.exception("Error clearing MVP schedule")
        return f"An error occurred: {str(e)}"

def get_response(user_input: str) -> str:
    try:
        cleaned_input = " ".join(user_input.split())
        lowered = cleaned_input.lower().strip()
        mvp_data = read_mvp_data(MVP_DATA_FILE)
        if lowered == '':
            return 'Blank input received'
        if lowered.startswith('-mvp'):
            return handle_mvp_command(lowered, cleaned_input, mvp_data)
        return choice(['I do not understand...', 'Try again'])
    except Exception as e:
        logger.exception("Error processing response")
        return f"An error occurred: {str(e)}"

def handle_mvp_command(lowered, cleaned_input, mvp_data):
    command_parts = lowered[4:].strip().split()
    command = command_parts[0]
    if command == 'hunt':
        return 'Let the hunt begin!'
    if command == 'dice':
        return f'You rolled: {randint(1, 6)}'
    if command == 'codes':
        return format_data_for_display(mvp_data)
    if command == 'add':
        parsed_data, error = parse_add_command(cleaned_input, mvp_data)
        if error:
            logger.error("Error parsing add command: %s", error)
            return f"Error: {error}"
        return add_or_update_mvp_sched(parsed_data, mvp_data, MVP_SCHED_FILE)
    if command == 'sched':
        mvp_sched = read_mvp_sched(MVP_SCHED_FILE)
        return format_sched_for_display(mvp_sched)
    if command == 'delete':
        if len(command_parts) < 2 or not command_parts[1].isdigit():
            return "Invalid format. Expected: -mvp delete {index}"
        index = int(command_parts[1])
        return delete_from_mvp_sched(index, MVP_SCHED_FILE)
    if command == 'clear':
        return clear_mvp_sched(MVP_SCHED_FILE)
    if command == 'help':
        return (
            "Available commands:\n"
            "-mvp hunt: Start the hunt.\n"
            "-mvp dice: Roll a dice.\n"
            "-mvp codes: Display MVP data.\n"
            "-mvp add: Add or update an MVP in the schedule.\n"
            "-mvp sched: Display the MVP schedule in a code block.\n"
            "-mvp delete {index}: Delete an entry from the schedule by index.\n"
            "-mvp clear: Clear all entries from the MVP schedule.\n"
            "-mvp help: Show this help message."
        )
    return 'Invalid MVP command. Try -mvp hunt, -mvp dice, -mvp codes, -mvp add, -mvp sched, -mvp delete {index}, -mvp clear, or -mvp help.'
