import os
import time
import explain_powerpoint
import requests

WEB_APP_URL = "http://127.0.0.1:5000/"

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
        # Step 1: Query the web app to get pending uploads
        url = f"{WEB_APP_URL}/get_pending_uploads"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            pending_uploads = data["pending_uploads"]
            for upload in pending_uploads:
                uid = upload["uid"]
                filename = upload["filename"]
                email = upload["email"]

                print(f"Processing upload: {uid}")

                # Step 2: Process the file using your existing functions (pptx parsing and GPT querying)
                explanation = explain_powerpoint.explain_powerpoint_func(UPLOADS_FOLDER + "\\" + filename)
                print(explanation)

                # Step 3: Update upload status and finish time in the web app
                url = f"{WEB_APP_URL}/update_upload_status"
                data = {
                    "uid": uid,
                    "status": "done",
                    "explanation": explanation
                }
                response = requests.post(url, json=data)

                if response.status_code == 200:
                    print(f"Upload '{uid}' processed and status updated.")
                else:
                    print(f"Failed to update status for upload '{uid}': {response.status_code} - {response.text}")

        else:
            print(f"Failed to fetch pending uploads: {response.status_code} - {response.text}")

        time.sleep(10)


if __name__ == "__main__":
    explainer()
