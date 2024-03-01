# logic you use to return a response of choice
# Implement logic for determining fact, cap, or uncertain
from random import choice, randint


def handle_response(message) -> str:
    # Just returns the message the user replied to for now
    # TODO: Implement AI algorithm
    p_message: str = message.lower()
    return p_message

