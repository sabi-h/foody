from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import io

app = Flask(__name__)

# This is the path to the directory where you want to save the uploaded files

UPLOAD_FOLDER = "images/"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_macronutrients(text):
    return "nothing yet..."


def get_objects():
    pass


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")  # Use .get to avoid KeyError if 'file' isn't in the form
    text_input = request.form.get("text_input")  # Retrieve text input from form

    filename = None
    if file and file.filename != "":
        # If the user does upload a file, process it
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    macronutrients = get_macronutrients(text_input)
    print(text_input)
    # Return success message with the uploaded filename (if any) and the text
    return jsonify(
        {"success": "Text received", "filename": filename if filename else "No file uploaded", "text": text_input}
    )


@app.route("/")
def hello_world():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7007)
