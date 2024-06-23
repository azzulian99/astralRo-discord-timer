import csv
from random import choice, randint

# Function to read the CSV file and get MVP data
def read_mvp_data(file_path: str):
    mvp_list = []
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                mvp_list.append((row['MVP'], row['MVP Short']))
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return mvp_list

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower().strip()

    if lowered == '':
        return 'Blank input received'
    elif lowered.startswith('-mvp'):
        command = lowered[4:].strip()  # Extract the command after '-mvp'
        
        if command == 'hunt':
            return 'Let the hunt begin!'
        elif command == 'dice':
            return f'You rolled: {randint(1, 6)}'
        elif command == 'codes':
            mvp_data = read_mvp_data('mvp_data.csv')
            if mvp_data:
                response = "MVP Codes:\n"
                response += "\n".join([f"{mvp} ({short})" for mvp, short in mvp_data])
                return response
            else:
                return "Failed to retrieve MVP data."
        elif command == 'help':
            return (
                "Available commands:\n"
                "-mvp hunt: Start the hunt.\n"
                "-mvp dice: Roll a dice.\n"
                "-mvp codes: Display MVP codes.\n"
                "-mvp help: Show this help message."
            )
        else:
            return 'Invalid MVP command. Try -mvp hunt, -mvp dice, -mvp codes, or -mvp help.'
    else:
        return choice(['I do not understand...', 'Try again'])

# Example test cases
if __name__ == "__main__":
    print(get_response('-mvp hunt'))  # Expected: 'Let the hunt begin!'
    print(get_response('-mvp dice'))  # Expected: 'You rolled: X' where X is a number between 1 and 6
    print(get_response('-mvp codes'))  # Expected: List of MVP and MVP Short
    print(get_response('-mvp help'))  # Expected: Help message with available commands
    print(get_response('random text'))  # Expected: Random response from ['I do not understand...', 'Try again']
