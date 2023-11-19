import werkzeug.datastructures
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from openai import OpenAI

from services.image_service import ImageService

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print(os.getenv("OPENAI_API_KEY"))
app = Flask(__name__)


# This is the path to the directory where you want to save the uploaded files

UPLOAD_FOLDER = "images/"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_macronutrients_by_text(text: str):
    print(text)

    openai_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"what are the macro nutrients in {text}"}]
    )

    print(openai_completion)

    if "choices" in openai_completion and openai_completion["choices"]:
        return openai_completion["choices"][0]["message"]["content"]
    else:
        print("something went wrong")


def get_macronutrients_by_image(image_file: werkzeug.datastructures.FileStorage):
    resized_image = ImageService.resize(image_file.read())
    base64_image = ImageService.encode_image(resized_image)

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": "identify all food ingredients in this picture and give me all macronutrients and their estimate values per 100 grams."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    print(response)

    return response


def save_file(file):
    file_path = None
    if file and file.filename != "":
        # If the user does upload a file, process it
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        file.save(file_path)

    return file_path


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")  # Use .get to avoid KeyError if 'file' isn't in the form
    text_input = request.form.get("text_input")  # Retrieve text input from form

    macronutrients_from_text = get_macronutrients_by_text(text_input)
    # macronutrients_from_image = get_macronutrients_by_image(file)

    return render_template("display_text.html", text='macronutrients_from_text')


@app.route("/")
def main():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
