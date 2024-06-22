import random

def handle_response (message) -> str:
    p_message = message.lower()

    if p_message == 'hello':
        return 'wassup bitch!'
    
    if p_message == 'dice':
        return (str.random.randint(1,6))
    
    if p_message == '!help':
        return '`This is help message that you can modify -TODO'
    