import os
from .embedder import extract_text, chunk_text, embed

_supabase = None


def get_supabase():
    """Initialize Supabase client only when first needed."""
    global _supabase
    if _supabase is None:
        from supabase import create_client
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
        _supabase = create_client(url, key)
    return _supabase


def upload_file(file_path: str) -> str:
    """
    Full RAG ingestion pipeline:
    Args:
        file_path: path to the file to ingest
    Returns:
        Arabic confirmation message
    """
    filename = os.path.basename(file_path)
    print(f"[RAG] Processing: {filename}")

    # Step 1: Extract
    text = extract_text(file_path)
    if not text.strip():
        return f"تعذّر استخراج نص من الملف '{filename}'."
    print(f"[RAG] Extracted {len(text)} characters")

    # Step 2: Chunk
    chunks = chunk_text(text)
    print(f"[RAG] Split into {len(chunks)} chunks")

    # Step 3: Embed (batch)
    embeddings = embed(chunks)
    print(f"[RAG] Embeddings generated")

    # Step 4: Store
    rows = [
        {
            "filename": filename,
            "content": chunk,
            "embedding": embedding,
        }
        for chunk, embedding in zip(chunks, embeddings)
    ]
    get_supabase().table("documents").insert(rows).execute()
    print(f"[RAG] Stored in Supabase")

    return f"تم رفع الملف '{filename}' بنجاح ({len(chunks)} قسم)"