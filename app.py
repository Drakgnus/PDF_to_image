from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
import io, base64

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert_pdf():

    if not request.files:
        return jsonify({
            "error": "Nenhum arquivo recebido",
            "content_type": request.content_type
        }), 400

    # pega QUALQUER arquivo enviado (n8n-safe)
    file = next(iter(request.files.values()))

    pdf_bytes = file.read()

    if not pdf_bytes:
        return jsonify({"error": "Arquivo vazio"}), 400

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
