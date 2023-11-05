from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import io
import openai

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# This is the path to the directory where you want to save the uploaded files

UPLOAD_FOLDER = "images/"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_macronutrients(text):
    openai_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"what are the macro nutrients in {text}"}
        ]
    )
    if "content" in openai_completion:
        return openai_completion["content"]
    else:
        raise Exception("No content in openai's response")


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
    return render_template("display_text.html", text=macronutrients)


@app.route("/")
def main():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7007)
