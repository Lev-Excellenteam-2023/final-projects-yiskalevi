import os
import read_data_from_powerPoint
import ask_answer_from_chatGPT
import asyncio

import Converts_list_to_file
Introduction_message_to_chatGPT="I have a presentation that I need to study, can you help me? I will send you every time all the information found in the current slide and you will explain to me what it says, ok?"

def main():
    path_of_the_powerPoint=input("give a path for the PowerPoint\n")
    if not (os.path.isfile(path_of_the_powerPoint) and path_of_the_powerPoint.endswith('.pptx')):
        path_of_the_powerPoint = input("The path is incorrect, please give a new path\n")
    slides=read_data_from_powerPoint.read_slides_from_presentation(path_of_the_powerPoint)
    questions = [Introduction_message_to_chatGPT] + slides  # Create a new list with Introduction_message_to_chatGPT as the first element
    list_of_responses = asyncio.run(ask_answer_from_chatGPT.list_question_to_the_chatGPT(questions))
    json_file=Converts_list_to_file.Converts_list_to_JSON_file(list_of_responses)
    print(json_file)





if __name__ == "__main__":
    main()


