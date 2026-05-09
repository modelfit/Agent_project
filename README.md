# Agent Project

## TODO

- [ ] Create a basic Google ADK agent architecture
- [ ] Add RAG system using Supabase DB
- [ ] Link cloud-based OCR for unparsable documents
- [ ] Link Google Gmail to agent (read/write access)
- [ ] Hijri to Gregorian conversion
- [ ] Calculator tool

## Optional

- [ ] Voice assistant
- [ ] Identity markdown files
- [ ] CRONs and heartbeat mechanism

## File Structure

```
projects/
├── README.md
├── upload.py                  ← CLI: ingest files into RAG
├── supabase_setup.sql         ← run once in Supabase dashboard
├── requirements.txt
├── .env                       ← your secrets (never commit this)
└── my_agent/
    ├── __init__.py
    ├── agent.py               ← main agent — do not modify
    ├── prompt.py              ← system prompt
    ├── memory.py              ← session service
    ├── tools/
    │   ├── __init__.py        ← register tools here only
    │   ├── calculator_tool.py
    │   ├── hijri_tool.py
    │   ├── reminder_tool.py
    │   ├── email_tool.py
    │   ├── rag_tool.py
    └── rag/
        ├── __init__.py
        ├── embedder.py        ← OCR + chunking + embedding
        ├── uploader.py        ← file → Supabase pipeline
        └── retriever.py       ← vector search
```

---

## Prerequisites

- Python 3.11 or higher
- A Google Cloud project with Gmail API enabled (for Gmail tool)

---

## 1. Clone and Set Up Environment

```powershell
# Navigate to your projects folder
cd C:\Users\YourName\projects

# Create a virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate

# You should now see (venv) in your prompt
```

---

## 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

`requirements.txt` contents:
```
google-adk
litellm
python-dotenv
supabase
pymupdf
docx2txt
langchain-text-splitters
hijridate
```

---

## 3. Configure Environment Variables

Create a `.env` file in the `projects/` root (same level as `my_agent/`):

```env
# OpenRouter
OPENROUTER_API_KEY=sk-or-your-key-here

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here

# Google OAuth (for Gmail — see Section 5)
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
```

> **Important:** Never commit `.env` to Git. Add it to `.gitignore`.

---

## 4. Set Up Supabase

1. Go to [supabase.com](https://supabase.com) and open your project
2. Click **SQL Editor** in the left sidebar
3. Paste the contents of `supabase_setup.sql` and click **Run**

This creates:
- The `documents` table with `pgvector` support
- A similarity search function `match_documents()`
- An index for fast vector search

---

## 5. Set Up Gmail (Google Cloud)

The ADK Gmail tool uses OAuth 2.0. Follow these steps once:

### 5a. Create a Google Cloud Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (or use an existing one)
3. Go to **APIs & Services → Enable APIs**
4. Search for **Gmail API** and enable it

### 5b. Create OAuth Credentials

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth Client ID**
3. Application type: **Desktop App**
4. Download the JSON file and rename it to `credentials.json`
5. Place `credentials.json` in the `projects/` root folder

### 5c. Add OAuth Scopes

1. Go to **APIs & Services → OAuth consent screen**
2. Add these scopes:
   - `https://www.googleapis.com/auth/gmail.send`
   - `https://www.googleapis.com/auth/gmail.readonly`
3. Add your Gmail address as a **Test User**

### 5d. First-time Auth

On first run the agent will open a browser window asking you to log in and grant access. After that, a `token.json` file is saved locally and reused automatically.

---

## 6. Upload Files to RAG (Optional)

To add documents to the knowledge base before running the agent:

```powershell
# Make sure venv is active
.\venv\Scripts\Activate

# Upload a PDF
python upload.py path\to\document.pdf

# Upload an image (OCR will extract text)
python upload.py path\to\scan.png

# Upload a Word document
python upload.py path\to\file.docx
```

Supported formats: `.pdf`, `.docx`, `.txt`, `.png`, `.jpg`, `.jpeg`

Scanned/image-based PDFs are automatically detected and sent to OCR.

---

## 7. Running the Agent

> Make sure your virtual environment is active and you are in the `projects/` folder before running either command.

```powershell
cd C:\Users\YourName\projects
.\venv\Scripts\Activate
```

### Option A — Terminal (PowerShell)

Simple back-and-forth chat directly in the terminal.

```powershell
adk run my_agent
```

Example session:
```
Running agent root_agent, type exit to exit.
[user]: كم ناتج 15 × 8؟
[agent]: ناتج 15 × 8 = 120
[user]: حوّل 2024/3/15 إلى هجري
[agent]: 15 مارس 2024 يوافق 5 رمضان 1445 هـ
[user]: exit
```

### Option B — Web UI (Recommended)

Full chat interface in the browser with tool call inspector.

```powershell
adk web
```

Then open your browser and go to:
```
http://localhost:8000
```

The web UI shows:
- Full chat interface
- Tool calls in real time (what tool was called, what args were passed)
- Session state inspector
- Easy to reset conversations

> Use `Ctrl+C` in PowerShell to stop the server.

---

## 8. Adding a New Tool

You only need to touch **two files**. `agent.py` is never modified.

### Step 1 — Copy the template

```powershell
copy my_agent\tools\TOOL_TEMPLATE.py my_agent\tools\your_tool_name.py
```

### Step 2 — Write your function

Open `my_agent/tools/your_tool_name.py` and fill in:

```python
def your_function_name(param1: str) -> str:
    """
    وصف قصير للأداة — يُستخدم من قِبل النموذج لفهم متى يستدعيها.

    Args:
        param1: وصف المعامل
    """
    # your logic here
    return "النتيجة"
```

### Step 3 — Register in `tools/__init__.py`

Add two lines:

```python
from .your_tool_name import your_function_name   # add this import

all_tools = [
    calculator,
    convert_to_hijri,
    set_reminder,
    write_email,
    search_documents,
    your_function_name,   # add your function here
]
```

### Step 4 — Test

```powershell
adk run my_agent
```

Ask the agent to use your tool and verify it calls it correctly.

---

## 9. Switching OCR Provider

The agent currently uses **Qianfan OCR** (free, for testing). To switch to **Gemini Flash** (recommended for Arabic in production):

Open `my_agent/rag/embedder.py` and change one line at the bottom of the OCR section:

```python
# current (testing):
_ocr_fn = ocr_with_qianfan

# production (better Arabic support):
_ocr_fn = ocr_with_gemini
```

No other changes needed.

---

## 10. Troubleshooting

### `ValueError: Model not found`
- The model string in `agent.py` is wrong or LiteLLM doesn't recognize it yet
- Run `pip install --upgrade litellm` then try again

### `adk` command not found
- Your virtual environment is not active
- Run `.\venv\Scripts\Activate` first

### `adk run` uses old agent code
- `adk run my_agent` reads from the file on disk, not from notebook cells
- Make sure you saved `agent.py` after editing

### Gmail auth fails
- Make sure `credentials.json` is in the `projects/` root
- Make sure your Gmail is added as a Test User in Google Cloud Console
- Delete `token.json` and re-authenticate if the token is stale

### Supabase returns empty results
- Check that `supabase_setup.sql` was run successfully
- Check that you uploaded at least one file using `upload.py`
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env` are correct

### OCR returns garbled Arabic
- Switch to Gemini Flash OCR (see Section 9)
- Qianfan is optimized for Chinese; Arabic results may be inconsistent

---

## Notes

- `agent.py` — never modify after initial setup
- `tools/__init__.py` — the only shared file collaborators touch
- `prompt.py` — owned by the project lead
- `.env` — never commit to Git, each developer has their own
- `token.json` — auto-generated after Gmail auth, do not commit