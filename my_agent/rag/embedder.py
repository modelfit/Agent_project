import os
import base64
import fitz 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..memory import _model, _lock


def ocr_with_qianfan(base64_image: str) -> str:
    """
    Extract text from image using Baidu Qianfan OCR.
    """
    import litellm
    response = litellm.completion(
        model="openrouter/baidu/qianfan-ocr-fast:free",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        api_base="https://openrouter.ai/api/v1",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                },
                {
                    "type": "text",
                    "text": "Extract all text from this image as-is."
                },
            ],
        }],
    )
    return response.choices[0].message.content

_ocr_fn = ocr_with_qianfan


def pdf_to_images(file_path: str) -> list[str]:
    """
    Convert each PDF page to a base64-encoded PNG.
    Used when a PDF is scanned and has no text layer.
    """
    doc = fitz.open(file_path)
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        images.append(base64.b64encode(img_bytes).decode("utf-8"))
    return images

def extract_text(file_path: str) -> str:
    """
    Extracts text from a file.

    Logic:
        .txt  → read directly
        .docx → docx2txt
        .pdf  → try text layer first
                if < 100 chars → scanned PDF → OCR each page
        image → OCR directly

    Supported: .txt, .docx, .pdf, .png, .jpg, .jpeg
    """
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif file_path.endswith(".docx"):
        import docx2txt
        return docx2txt.process(file_path)

    elif file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        text = "\n".join(page.get_text() for page in doc).strip()
        print("Scanning pdf with OCR...")
        images = pdf_to_images(file_path)
        text = "\n\n".join(_ocr_fn(img) for img in images)

        return text

    elif file_path.endswith((".png", ".jpg", ".jpeg")):
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return _ocr_fn(b64)

    else:
        raise ValueError(f"Unsupported file type: {file_path}")


def chunk_text(text: str) -> list[str]:
    """
    Text chuncking using Recursive character splitter by langchain

    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=250,
    )
    return splitter.split_text(text)


def embed(texts: list[str]) -> list[list[float]]:
    """
    Embeds a list of text chunks using IBM Granite.

    Args:
        texts: list of text chunks to embed
    Returns:
        list of 768-dim vectors, one per chunk
    """
    with _lock:
        embeddings = _model.encode(texts, normalize_embeddings=True)
    return [e.tolist() for e in embeddings]