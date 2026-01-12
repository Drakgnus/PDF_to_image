from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
import io
import base64

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert_pdf():
    pdf_bytes = None

    # 1️⃣ multipart/form-data (file)
    if "file" in request.files:
        pdf_bytes = request.files["file"].read()

    # 2️⃣ binário bruto (application/pdf)
    elif request.content_type == "application/pdf":
        pdf_bytes = request.data

    # 3️⃣ base64 (JSON)
    elif request.is_json and "base64" in request.json:
        pdf_bytes = base64.b64decode(request.json["base64"])

    if not pdf_bytes:
        return jsonify({"error": "Nenhum PDF recebido"}), 400

    images = convert_from_bytes(pdf_bytes, dpi=200)

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
