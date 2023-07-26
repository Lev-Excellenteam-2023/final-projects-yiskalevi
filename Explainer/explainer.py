import os
import time

import explain_powerpoint


UPLOADS_FOLDER = "C:\\networks\\excelantim\\project1\\uploads"
OUTPUTS_FOLDER = "C:\\networks\\excelantim\\project1\\outputs"


def write_json_to_file(json_string, file_path):
    with open(file_path, "w") as f:
        f.write(json_string)


def process_files():
    """
    Process the files in the 'uploads' folder and save the explanation JSON in the 'outputs' folder.
    """
    # Get the list of files in the 'uploads' folder
    uploaded_files = os.listdir(UPLOADS_FOLDER)

    for file in uploaded_files:
        # file_path = os.path.join(UPLOADS_FOLDER, file)
        fileName = os.path.splitext(file)[0]
        # Check if the file exists in the 'outputs' folder
        if os.path.exists(os.path.join(OUTPUTS_FOLDER, fileName + ".json")):
            continue

        print(f"Processing file: {file}")
        # Step 2: Process the file using your existing functions (pptx parsing and GPT querying)
        explanation = explain_powerpoint.explain_powerpoint_func(UPLOADS_FOLDER + "\\" + file)
        print(explanation)

        write_json_to_file(explanation, OUTPUTS_FOLDER + "\\" + fileName + ".json")

        print(f"File '{file}' processed and explanation saved.")


def explainer():
    """
    The main function that runs the explainer system indefinitely.
    """
    while True:
        process_files()
        time.sleep(10)


if __name__ == "__main__":
    explainer()
