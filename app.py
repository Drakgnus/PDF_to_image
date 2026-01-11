from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
import io, base64

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert_pdf():
    return {
        "content_type": request.content_type,
        "headers": dict(request.headers),
        "files_keys": list(request.files.keys()),
        "form_keys": list(request.form.keys()),
        "raw_length": request.content_length,
    }, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
