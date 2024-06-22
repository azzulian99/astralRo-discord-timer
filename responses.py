from random import choice, randint

def get_response(user_input : str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Blank input received'
    elif 'hunt' in lowered:
        return 'Let the hunt begin!'
    elif 'dice' in lowered:
        return  f'You rolled: {randint(1,6)}'
    else:
        return choice(['I do not understand...'],
                      ['Try again'])