import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

UPLOADS_FOLDER = "C:\\networks\\excelantim\\project1\\uploads"
OUTPUTS_FOLDER = "C:\\networks\\excelantim\\project1\\outputs"

if not os.path.exists(UPLOADS_FOLDER):
    os.makedirs(UPLOADS_FOLDER)

if not os.path.exists(OUTPUTS_FOLDER):
    os.makedirs(OUTPUTS_FOLDER)


def generate_unique_filename(original_filename):
    """
    Generate a unique filename for an uploaded file.

    Parameters:
        original_filename (str): The original filename of the uploaded file.

    Returns:
        str: A new filename with a unique ID and timestamp, keeping the original file extension.

    This function takes the original filename of an uploaded file and appends a unique
    ID and timestamp to it, creating a new filename that is guaranteed to be unique.

    The generated filename format is: "<original_filename_without_extension>_<timestamp>_<unique_id>.<file_extension>"

    Example:
        If the original filename is "presentation.pptx", and the function is called at
        2023-07-23 15:30:00, the returned filename might be:
        "presentation_20230723_153000_85f0dce290ea4b38a27bdc1c7fb0b3c3.pptx"
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4().hex)
    filename_without_extension, file_extension = os.path.splitext(original_filename)
    return f"{filename_without_extension}_{timestamp}_{unique_id}{file_extension}"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    """
    Handle file upload from a POST request.

    Returns:
        Response: A JSON response with the UID of the uploaded file.

    This function receives a POST request with an attached file. It generates a unique
    filename for the uploaded file using the generate_unique_filename function. The file
    is then saved in the "uploads" folder. The function returns a JSON response containing
    the UID of the uploaded file.

    If there is no file part in the request or no selected file, the function returns
    a JSON error response with a status code 400 (Bad Request).

    Example:
        POST request with an attached file named "presentation.pptx" returns:
        {"uid": "presentation.pptx_20230723_153000_85f0dce290ea4b38a27bdc1c7fb0b3c3"}
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = (uploaded_file.filename)
    uid = generate_unique_filename(filename)
    file_path = os.path.join(UPLOADS_FOLDER, uid)
    uploaded_file.save(file_path)

    return jsonify({uid: filename}), 200


@app.route("/status/<string:uid>", methods=["GET"])
def get_status(uid):
    """
    Get the status of an uploaded file.

    Parameters:
        uid (str): The UID of the uploaded file.

    Returns:
        Response: A JSON response with the status, filename, timestamp, and explanation.

    This function receives a GET request with a UID as a URL parameter. It checks if
    the file with the given UID exists in the "uploads" folder. If the file exists, it
    checks if there is a corresponding output file in the "outputs" folder. If the output
    file exists, it reads the explanation from the file and returns a JSON response with
    the status set to "done" and the explanation.

    If the file with the given UID does not exist in the "uploads" folder, the function
    returns a JSON response with the status set to "not found" and a status code 404 (Not Found).

    If the output file does not exist yet, the function returns a JSON response with the
    status set to "pending" and the explanation set to None.

    Example:
        GET request with UID "presentation.pptx_20230723_153000_85f0dce290ea4b38a27bdc1c7fb0b3c3"
        returns:
        {
            "status": "done",
            "filename": "presentation.pptx_20230723_153000_85f0dce290ea4b38a27bdc1c7fb0b3c3",
            "timestamp": "",
            "explanation": "The explanation content goes here..."
        }
    """
    file_path = os.path.join(UPLOADS_FOLDER, uid)
    if not os.path.exists(file_path):
        return jsonify({"status": "not found"}), 404

    output_file_path = os.path.join(OUTPUTS_FOLDER, os.path.splitext(uid)[0] + ".json")

    filename = uid.split('_')[0]
    timestamp = uid.split('_')[1] + "_" + uid.split('_')[2]  # Extract timestamp from the UID

    if os.path.exists(output_file_path):
        with open(output_file_path, "r") as f:
            explanation = f.read()
        return jsonify(
            {"status": "done", "filename": filename, "timestamp": timestamp, "explanation": explanation}), 200
    else:
        return jsonify({"status": "pending", "filename": filename, "timestamp": timestamp, "explanation": None}), 200


if __name__ == "__main__":
    app.run(debug=True)
