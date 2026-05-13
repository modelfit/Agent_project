"""
upload_server.py — receives file uploads from the HTML frontend
and passes them through the RAG ingestion pipeline.

Run alongside adk api_server:
    Terminal 1: adk api_server my_agent --allow_origins="*"
    Terminal 2: python upload_server.py
"""

import os
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# Import RAG uploader
from my_agent.rag.uploader import upload_file

app = Flask(__name__)
CORS(app)  # Allow requests from the HTML frontend

ALLOWED_EXTENSIONS = {"pdf", "txt", "docx", "png", "jpg", "jpeg"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload():
    """
    Receives a file from the frontend, saves it temporarily,
    runs it through the RAG pipeline, then deletes the temp file.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": f"File type not supported. Allowed: {ALLOWED_EXTENSIONS}"}), 400

    # Save to temp file
    suffix = "." + file.filename.rsplit(".", 1)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        # Run through RAG pipeline
        result = upload_file(tmp_path)

        # Rename for accurate filename in DB
        import shutil
        named_path = tmp_path.replace(os.path.basename(tmp_path), file.filename)
        shutil.copy(tmp_path, named_path)
        result = upload_file(named_path)
        os.unlink(named_path)

        return jsonify({"message": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Always clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    print("Upload server running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
