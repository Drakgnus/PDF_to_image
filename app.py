from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
from pdfminer.high_level import extract_text
import io
import base64
import tempfile

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert_pdf():
    pdf_bytes = None

    # 1️⃣ multipart/form-data (file)
    if request.files:
        pdf_bytes = next(iter(request.files.values())).read()

    # 2️⃣ binário bruto (application/pdf)
    elif request.content_type == "application/pdf":
        pdf_bytes = request.data

    # 3️⃣ base64 (JSON)
    elif request.is_json and "base64" in request.json:
        pdf_bytes = base64.b64decode(request.json["base64"])

    if not pdf_bytes:
        return jsonify({"error": "Nenhum PDF recebido"}), 400

    # 🔍 TENTA EXTRAIR TEXTO (contexto)
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        tmp.flush()
        text = extract_text(tmp.name) or ""

    # 👉 CASO TENHA TEXTO
    if text.strip():
        return jsonify({
            "has_text": True,
            "text": text
        })

    # 👉 CASO NÃO TENHA TEXTO → converte para imagem
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
        "has_text": False,
        "pages": len(result),
        "images": result
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
