from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import handle_response

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
# No Quality Assurance : suppresses warnings
intents.message_content = True # NOQA

client: Client = Client(intents=intents)

# Message Functionality
async def send_message(message, user_message: str) -> None:
    if not user_message:
        print("Message was empty because intents were not enabled (probaby)")
        return

    if user_message.startswith('!cap') and message.reference is not None:
        try:
            replied_message = await message.channel.fetch_message(message.reference.message_id)
            if replied_message is not None and replied_message.author != client.user:
                response: str = handle_response(replied_message.content)
                await message.channel.send(response)
        # TODO: Not good practice. Want to be as specific as possible with exceptions. Should change
        except Exception as e:
            print(e)

# Bot Start Up
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running')

# Handle Incoming messages
@client.event
async def on_message(message: Message) -> None:
    # If the message is made by the bot, then we should not respond to it. It would result in an infinite loop
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = str(message.content)
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)


# Entry Point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()



