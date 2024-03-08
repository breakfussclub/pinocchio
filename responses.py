from openai import OpenAI
import tiktoken

def handle_response(message) -> str:
    p_message: str = message.lower()

    return askgpt(message)


# single-turn task
def askgpt(message) -> int:
    client = OpenAI()

    setupmessage = "You are a fact checker. I will give you a message, \
                    if there are multiple claims, respond with 'There are multiple claims', \
                    otherwise, respond with one of these options: \
                    True, False, I don't know, That is an opinion. \
                    Pick the one you're most sure about."
                    
                    # '1' for True, \
                    # '2' for False, \
                    # '3' if you don't know, \
                    # '4' if the message is an opinion, \
                    # '5' if there are multiple claims. \
                    # Remember, respond with only a number between \
                    # 1-5 corresponding to the answer you're most \
                    # sure of."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": setupmessage},
            {"role": "user", "content": message}
        ]
    )

    print(f'{response.usage.prompt_tokens} prompt tokens used.')

    # TODO: catch error
    answer = response.choices[0].message.content

    return answer


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0613":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
    See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


testmessages = [
    "grass is green",
    "apples are red",
    "the sky is red",
    "grass is green and teh sky is blue",
    "you’re terrible at French",
    "most people experience phobias, and all phobias are caused by past trauma",
]

for message in testmessages:
    print(f'{message}: {askgpt(message)}')