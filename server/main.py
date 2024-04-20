import logging
from flask import Flask, request, jsonify
from recognition.image_recognition import recognize
from recognition.text_recognition import process_user_input
from models import sights

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


@app.route("/sight/map")
def get_map():
    request_body = request.get_json()
    sight = sights[request_body.get("sight_name")]
    link = f'https://2gis.kz/astana/geo/{sight["2gis_id"]}/{sight["2gis_coord_f"]}%2C{sight["2gis_coord_s"]}'
    return jsonify({'2gis_link': link})


@app.route("/recognize_input")
def recognize_input():
    request_body = request.get_json()
    user_input = request_body.get("user_input")
    language, sug_input = process_user_input(user_input)
    return jsonify({'language': language, 'suggested_input': sug_input})

@app.route("/sight/route")
def get_route():
    request_body = request.get_json()
    sight = sights[request_body.get("sight_name")]
    longitude = request_body.get('longitude')
    latitude = request_body.get('latitude')
    link = f'https://2gis.kz/astana/directions/points/{longitude}%2C{latitude}%7C{sight["2gis_coord_f"]}%2C{sight["2gis_coord_s"]}%3B{sight["2gis_id"]}'
    return jsonify({'2gis_route': link})


@app.route("/sight/<name>")
def get_sight(name: str):
    return jsonify(sights[name.lower()])



@app.route("/", methods=["POST"])
def post_root():
    request_body = request.get_json()
    return jsonify({"sight_name": request_body.get("sight_name"), "user_geolocation": request_body.get("user_geolocation")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
