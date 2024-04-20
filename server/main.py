import logging
from flask import Flask, request, jsonify
from recognition.image_recognition import recognize

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route("/recognize_image", methods=["POST"])
def recognize_image():
    try:
        if 'image' not in request.files:
            return "No image provided", 400

        image_file = request.files['image']

        if image_file.filename == '':
            return "No image selected", 400

        image_path = "/tmp/uploaded_image.jpg"
        image_file.save(image_path)

        class_name, conf_score = recognize(image_path)

        return jsonify({"message": class_name})
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return "Internal Server Error", 500


@app.route("/hello/<name>")
def say_hello(name):
    return jsonify({"message": f"Hello {name}"})

@app.route("/", methods=["POST"])
def post_root():
    request_body = request.get_json()
    return jsonify({"sight_name": request_body.get("sight_name"), "user_geolocation": request_body.get("user_geolocation")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
