import openai
import time

openai.api_key = "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"

def list_question_to_the_chatGPT(questions: list) -> list:
    """
    Sends a list of questions to the chatGPT model and returns the model's responses.
    """
    messages = [{"role": "system", "content": ''}]
    list_of_responses = []
    rate_limit_reached = False

    for question in questions:
        messages.append({"role": "user", "content": question})
        print(question)
        completion = None

        while not completion:
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
            except openai.error.RateLimitError as e:
                # print("Rate limit reached. Waiting for 20 seconds...")
                time.sleep(20)  # Wait for 20 seconds
                rate_limit_reached = True

        chat_response = completion.choices[0].message.content
        list_of_responses.append(chat_response)
        messages.append({"role": "assistant", "content": chat_response})

        if rate_limit_reached:
            # Reset the rate limit flag
            rate_limit_reached = False

    return list_of_responses[1:] #We will take down the message of the response and explanation that they sent in the chat.



