import os
import threading
from google.adk.sessions import InMemorySessionService
from sentence_transformers import SentenceTransformer

session_service = InMemorySessionService()

print("[Memory] Loading embedding model...")
_model = SentenceTransformer("ibm-granite/granite-embedding-278m-multilingual")
print("[Memory] Model ready.")

# Thread lock — prevents concurrent embedding calls
_lock = threading.Lock()

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


def embed_text(text: str) -> list[float]:
    """
    Converts text to a 768-dim vector using IBM Granite.

    Args:
        text: any text in Arabic or English
    Returns:
        list of 768 floats representing the text semantically
    """
    with _lock:
        embedding = _model.encode(text, normalize_embeddings=True)
        return embedding.tolist()


def save_memory(session_id: str, role: str, content: str):
    """
    Embeds and stores a conversation turn in Supabase.
    This is what builds the memory over time.

    Flow:
        text
          ↓
        embed_text() → 768-dim vector
          ↓
        Supabase chat_memory table
    """
    try:
        embedding = embed_text(content)
        get_supabase().table("chat_memory").insert({
            "session_id": session_id,
            "role": role,
            "content": content,
            "embedding": embedding,
        }).execute()
    except Exception as e:
        print(f"[Memory] Failed to save: {e}")


def search_memory(session_id: str, query: str, top_k: int = 5) -> list[dict]:
    """
    Finds the most semantically similar past messages.
    Uses cosine similarity — finds relevant memories even
    if the user uses different words than before.
    """
    try:
        query_embedding = embed_text(query)
        result = get_supabase().rpc("match_memory", {
            "query_embedding": query_embedding,
            "session_id_filter": session_id,
            "match_count": top_k,
        }).execute()
        return result.data
    except Exception as e:
        print(f"[Memory] Failed to search: {e}")
        return []


def format_memories(memories: list[dict]) -> str:
    """
    Converts raw memory results into a readable Arabic
    context block injected into the agent message.
    """
    if not memories:
        return ""

    lines = ["### ذكريات ذات صلة من محادثات سابقة:\n"]
    for m in memories:
        role_label = "المستخدم" if m["role"] == "user" else "المساعد"
        lines.append(f"- {role_label}: {m['content']}")

    return "\n".join(lines)


def load_recent(session_id: str, limit: int = 20) -> list[dict]:
    """Load last N messages in chronological order."""
    try:
        result = get_supabase().table("chat_memory") \
            .select("role, content, created_at") \
            .eq("session_id", session_id) \
            .order("created_at", desc=False) \
            .limit(limit) \
            .execute()
        return result.data
    except Exception as e:
        print(f"[Memory] Failed to load: {e}")
        return []

def clear_memory(session_id: str) -> str:
    """Delete all stored memory for a given session."""
    try:
        get_supabase().table("chat_memory") \
            .delete() \
            .eq("session_id", session_id) \
            .execute()
        return "تم مسح الذاكرة بنجاح."
    except Exception as e:
        return f"خطأ في مسح الذاكرة: {str(e)}"