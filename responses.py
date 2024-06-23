import csv
from datetime import datetime, timedelta
import re
from constants import MVP_DATA_FILE, MVP_SCHED_FILE
from fileUtils import read_mvp_data, read_mvp_sched, write_mvp_sched

# Function to parse and validate the input for the -mvp add command
def parse_add_command(user_input: str, mvp_data: dict):
    pattern = r'-mvp add (\w+) (\d{2}:\d{2}(?::\d{2})?) (\d{1,3}) (\d{1,3})( \d+)?'
    match = re.match(pattern, user_input)
    
    if not match:
        return None, "Invalid format. Expected: -mvp add {code} {currentDeathTime} {coordinateX} {coordinateY} {optional int}"
    
    code, death_time, x, y, optional_int = match.groups()[0], match.groups()[1], match.groups()[2], match.groups()[3], match.groups()[4]
    x = int(x)
    y = int(y)
    optional_int = int(optional_int.strip()) if optional_int else None
    
    if code not in mvp_data:
        return None, "Invalid MVP code."
    
    if not (0 <= x < 500 and 0 <= y < 500):
        return None, "Coordinates must be between 0 and 499."
    
    try:
        if len(death_time) == 5:  # hh:mm format
            death_time = datetime.strptime(death_time, '%H:%M')
        elif len(death_time) == 8:  # hh:mm:ss format
            death_time = datetime.strptime(death_time, '%H:%M:%S')
        else:
            return None, "Invalid time format. Expected hh:mm or hh:mm:ss."
    except ValueError:
        return None, "Invalid time format. Expected hh:mm or hh:mm:ss."
    
    return (code, death_time, x, y, optional_int), None

# Function to add an entry to the MVP schedule
def add_to_mvp_sched(parsed_data, mvp_data, mvp_sched_file):
    code, death_time, x, y, optional_int = parsed_data
    death_duration_start, death_duration_end, location = mvp_data[code]
    
    death_duration_start = timedelta(minutes=int(death_duration_start.split(':')[1]), hours=int(death_duration_start.split(':')[0]))
    death_duration_end = timedelta(minutes=int(death_duration_end.split(':')[1]), hours=int(death_duration_end.split(':')[0]))
    
    next_spawn_start = (death_time + death_duration_start).time()
    next_spawn_end = (death_time + death_duration_end).time()
    
    new_entry = {
        'MVP Code': code,
        'Next Spawn Start': next_spawn_start.strftime('%H:%M:%S'),
        'Next Spawn End': next_spawn_end.strftime('%H:%M:%S'),
        'Location': location,
        'Coordinates': f"{x} {y}"
    }
    
    mvp_sched = read_mvp_sched(mvp_sched_file)
    mvp_sched.append(new_entry)
    write_mvp_sched(mvp_sched_file, mvp_sched)
    
    return "Entry added successfully."

# Function to format the MVP data for display in a code block
def format_data_for_display(mvp_data):
    formatted_data = "MVP Data:\n"
    formatted_data += "MVP Code | Death Duration Start | Death Duration End | Location\n"
    formatted_data += "-" * 65 + "\n"
    for code, (start, end, location) in mvp_data.items():
        formatted_data += f"{code} | {start} | {end} | {location}\n"
    return f"```\n{formatted_data}\n```"

# Function to format the MVP schedule for display in a code block
def format_sched_for_display(mvp_sched):
    if not mvp_sched:
        return "MVP schedule is empty."
    
    formatted_sched = "MVP Schedule:\n"
    formatted_sched += "MVP Code | Next Spawn Start | Next Spawn End | Location & Coordinates\n"
    formatted_sched += "-" * 75 + "\n"
    for row in mvp_sched:
        location_and_coords = f"{row['Location']} ({row['Coordinates']})"
        formatted_sched += f"{row['MVP Code']} | {row['Next Spawn Start']} | {row['Next Spawn End']} | {location_and_coords}\n"
    return f"```\n{formatted_sched}\n```"

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower().strip()
    mvp_data = read_mvp_data(MVP_DATA_FILE)

    if lowered == '':
        return 'Blank input received'
    elif lowered.startswith('-mvp'):
        command = lowered[4:].strip()  # Extract the command after '-mvp'
        
        if command == 'hunt':
            return 'Let the hunt begin!'
        elif command == 'dice':
            return f'You rolled: {randint(1, 6)}'
        elif command == 'codes':
            return format_data_for_display(mvp_data)
        elif command.startswith('add'):
            parsed_data, error = parse_add_command(user_input, mvp_data)
            if error:
                return error
            return add_to_mvp_sched(parsed_data, mvp_data, MVP_SCHED_FILE)
        elif command == 'sched':
            mvp_sched = read_mvp_sched(MVP_SCHED_FILE)
            return format_sched_for_display(mvp_sched)
        elif command == 'help':
            return (
                "Available commands:\n"
                "-mvp hunt: Start the hunt.\n"
                "-mvp dice: Roll a dice.\n"
                "-mvp codes: Display MVP data.\n"
                "-mvp add: Add an MVP to the schedule.\n"
                "-mvp sched: Display the MVP schedule in a code block.\n"
                "-mvp help: Show this help message."
            )
        else:
            return 'Invalid MVP command. Try -mvp hunt, -mvp dice, -mvp codes, -mvp add, -mvp sched, or -mvp help.'
    else:
        return choice(['I do not understand...', 'Try again'])

# Example test cases
if __name__ == "__main__":
    print(get_response('-mvp hunt'))  # Expected: 'Let the hunt begin!'
    print(get_response('-mvp dice'))  # Expected: 'You rolled: X' where X is a number between 1 and 6
    print(get_response('-mvp codes'))  # Expected: List of MVP data
    print(get_response('-mvp add VR 14:30 120 340 3'))  # Expected: Entry added successfully.
    print(get_response('-mvp sched'))  # Expected: Formatted MVP schedule in a code block or "MVP schedule is empty."
    print(get_response('-mvp help'))  # Expected: Help message with available commands
    print(get_response('random text'))  # Expected: Random response from ['I do not understand...', 'Try again']
