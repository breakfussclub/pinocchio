# logic you use to return a response of choice
# Implement logic for determining fact, cap, or uncertain
from random import choice, randint


def handle_response(message) -> str:
    p_message: str = message.lower()

    # TODO: Implement AI algorithm
    if p_message == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in p_message:
        return 'Hey there!'
    elif 'rolldice' in p_message:
        return f'You rolled: {randint(1,6)}'
    else:
        return choice([
            'I dont understand...',
            'What are you talking about?'
        ])
