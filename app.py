from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
import io
import base64

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert_pdf():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "PDF não enviado"}), 400

    images = convert_from_bytes(file.read(), dpi=200)

    result = []
    for i, img in enumerate(images):
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        result.append({
            "page": i + 1,
            "image_base64": base64.b64encode(buffer.getvalue()).decode()
        })

    return jsonify({
        "pages": len(result),
        "images": result
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
