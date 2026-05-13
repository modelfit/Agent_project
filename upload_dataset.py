from dotenv import load_dotenv
load_dotenv()

from datasets import load_dataset
from my_agent.rag.embedder import chunk_text, embed
from my_agent.memory import get_supabase
from tqdm import tqdm

print("[HF] Loading dataset...")
ds = load_dataset("drelhaj/Arabic-news-and-management-corpus", "full_text")

dataset = ds['train']

supabase = get_supabase()

success = 0
failed = 0

for i, row in tqdm(enumerate(dataset)):
    try:
        text = str(row['text']).strip()
        if not text:
            continue

        chunks = chunk_text(text)

        embeddings = embed(chunks)

        rows = [
            {
                "filename": f"arabic-news-corpus:row_{i}:domain_{row['domain']}",
                "content":  chunks,
                "embedding": embeddings,
            }
            for chunks, embeddings in zip(chunks,embeddings)
        ]
        supabase.table("documents").insert(rows).execute()
        success += 1

    except Exception as e:
        print(f"failed to load dataset cause: {e}")
        failed += 1

print(f"inshallah done Success: {success} \n failed: {failed}")