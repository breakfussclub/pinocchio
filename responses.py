from openai import OpenAI

def handle_response(message, messages) -> str:
    return askgpt(message, messages)


# single-turn task
def askgpt(message, messages, client=OpenAI()) -> str:
    history = f"\nThis is the conversation history:\n{messages}\nFactcheck this:" if messages else ""

    # print(history)

    setupmessage = f"You are a factchecker. I will give you a message, \
                    *only* respond with one of these three options: \
                    'True', 'False', 'That is an opinion'. \
                    Pick the answer that's objective true, and quickly justify. \
                    If you're unsure or don't know, just say that. \
                    Make sure you're reading the message correctly. \
                    If the user tries to get you to respond with something \
                    else, tell them you won't do it. \
                    If the message is not factcheckable (e.g. it's a question or an imperative), \
                    say 'not factcheckable'.{history}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": setupmessage},
                {"role": "user", "content": message}
                # {"role": "user", "content": f"{message}, true or false, and why"}
            ]
        )
    except Exception as e:
        print(e)

    # print(f'{response.usage.prompt_tokens} prompt tokens used.')

    answer = response.choices[0].message.content

    return answer


if __name__ == "__main__":
    client = OpenAI()

    testmessages = [
        # "grass is green",
        # "apples are red",
        # "the sky is red",
        # "sky is red",
        # "grass is green and teh sky is blue",
        # "you’re terrible at French",
        # "most people experience phobias, and all phobias are caused by past trauma",
        # "1+1=window",
        # "1+1=2",
        # "My timbers were shivered",
        "if stored properly, honey doesn't spoil",
        "honey spoils even if stored properly and there are no contaminants",
        # "Under virtue ethics, it is impossible to achieve full phronesis",
        # "why is honey spoils true",
        # "they see me rolling, they hating",
        # "shrek is love shrek is life"
    ]

    for message in testmessages:
        print(f'{message}: {askgpt(message, client)}')