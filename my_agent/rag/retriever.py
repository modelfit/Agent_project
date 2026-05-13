import os
from ..memory import embed_text

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


def retrieve(query: str, top_k: int = 20) -> list[str]:
    """
    Document RAG retrieval pipeline:
    Args:
        query: the user's question or search term
        top_k: number of chunks to return (default: 20)
    Returns:
        list of relevant text chunks
    """
    query_embedding = embed_text(query)

    result = get_supabase().rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_count": top_k,
        },
    ).execute()

    return [row["content"] for row in result.data]