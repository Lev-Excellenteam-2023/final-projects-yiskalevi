import openai
import asyncio

api_key_file = 'api_key_file.txt'  # Replace with the path to your API key file

with open(api_key_file, 'r') as file:
    openai.api_key = file.read().strip()


async def generate_chat_response( messages):
    completion =openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    chat_response = completion.choices[0].message.content
    return chat_response

async def list_question_to_the_chatGPT(questions: list) -> list:
    """
    Sends a list of questions to the ChatGPT model asynchronously and returns the model's responses.
    """
    messages = [{"role": "system", "content": ""}]
    list_of_responses = []

    tasks = []
    for question in questions:
        messages.append({"role": "user", "content": question})
        task = generate_chat_response( messages.copy())
        tasks.append(task)

    responses = await asyncio.gather(*tasks)
    i=0
    for response in responses:
        messages.append({"role": "assistant", "content": response})
        list_of_responses.append(response)
        i=i+1

    return list_of_responses[1:]



