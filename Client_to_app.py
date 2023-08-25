import os
from datetime import datetime
from dataclasses import dataclass
import requests

WEB_APP_URL = "http://127.0.0.1:5000/"


@dataclass
class Status:
    status: str
    filename: str
    timestamp: datetime
    explanation: str

    def is_done(self):
        return self.status == "done"


class PythonClient:
    @staticmethod
    def upload(file_path: str, email: str = None) -> str:
        if not (os.path.isfile(file_path) and file_path.endswith('.pptx')):
            raise ValueError("The file is not a presentation")

        url = f"{WEB_APP_URL}/upload"
        data = {"email": email} if email else None
        with open(file_path, "rb") as file:
            response = requests.post(url, files={"file": file}, data=data)

        if response.status_code == 200:
            data = response.json()
            return list(data.keys())[0]
        else:
            raise Exception(f"Failed to upload file: {response.status_code} - {response.text}")

    @staticmethod
    def status(uid: str, email: str = None) -> Status:
        url = f"{WEB_APP_URL}/status"
        params = {"uid": uid, "email": email} if email else {"uid": uid}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            status = data["status"]
            filename = data["filename"]
            timestamp_str = data["timestamp"]
            explanation = data["explanation"]
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            return Status(status=status, filename=filename, timestamp=timestamp, explanation=explanation)
        else:
            raise Exception(f"Failed to get status: {response.status_code} - {response.text}")


if __name__ == "__main__":
    # Example usage:
    client = PythonClient()
    file_path = input("Enter the path of the PowerPoint file: ")
    email = input("Enter your email (optional): ")

    try:
        uid = client.upload(file_path, email)
        print(f"File uploaded successfully. UID: {uid}")

        # Wait for some time (e.g., 10 seconds) before checking status
        import time

        time.sleep(30)
        flag = True
        while flag:
            status = client.status(uid, email)
            if status.is_done():
                print(f"File processing is done.")
                print(f"Explanation: {status.explanation}")
                flag = False
            else:
                print(f"File processing is still pending.")
                time.sleep(30)
    except Exception as e:
        print(f"Error: {e}")
