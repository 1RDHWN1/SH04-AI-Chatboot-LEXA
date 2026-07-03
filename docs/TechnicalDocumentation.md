# Technical Documentation — SH04-AI-Chatbot-LEXA

**Project:** SH04-AI-Chatbot-LEXA  
**Version:** 1.0.0  
**Last Updated:** 2025-07-01  
**Audience:** Developers, Technical Reviewers

---

## 1. Project Architecture

```
SH04-AI-Chatbot-LEXA/
├── llm.py              ← Core LLM module (LexaChatbot class)
├── app.py              ← Streamlit web interface
├── main.py             ← CLI interface
├── requirements.txt    ← Python dependencies
├── .env                ← Environment variables (not committed)
└── README.md           ← Project overview
```

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     User Interfaces                      │
│                                                         │
│  ┌──────────────────┐    ┌──────────────────────────┐  │
│  │    main.py       │    │        app.py             │  │
│  │   (CLI mode)     │    │   (Streamlit Web UI)      │  │
│  │                  │    │                           │  │
│  │  Input loop      │    │  st.chat_input()          │  │
│  │  stdin/stdout    │    │  st.session_state         │  │
│  │  KeyboardInt.    │    │  Streaming placeholder    │  │
│  └────────┬─────────┘    └──────────┬────────────────┘  │
│           │                         │                    │
│           └──────────┬──────────────┘                    │
│                      │                                   │
│                      ▼                                   │
│          ┌───────────────────────┐                       │
│          │       llm.py          │                       │
│          │   LexaChatbot class   │                       │
│          │                       │                       │
│          │  __init__()           │                       │
│          │  send_message()       │                       │
│          │  send_message_stream()│                       │
│          │  reset_chat()         │                       │
│          └───────────┬───────────┘                       │
│                      │                                   │
└──────────────────────┼───────────────────────────────────┘
                       │  HTTPS
                       ▼
         ┌─────────────────────────────┐
         │      Groq Cloud API         │
         │  api.groq.com/v1/chat/...   │
         │  Model: gpt-oss-120b        │
         └─────────────────────────────┘
```

---

## 2. Module Documentation

### 2.1 `llm.py` — Core LLM Module

#### Class: `LexaChatbot`

The central class that wraps the Groq API client and manages conversation state.

**Constructor:**
```python
def __init__(self, system_instruction=None, model="openai/gpt-oss-120b")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `system_instruction` | `str \| None` | `None` | Custom system prompt. Uses default CS prompt if None. |
| `model` | `str` | `"openai/gpt-oss-120b"` | Groq model identifier. |

**Instance Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `api_key` | `str` | Groq API key loaded from environment |
| `client` | `groq.Groq` | Initialized Groq SDK client |
| `model` | `str` | Active model name |
| `system_instruction` | `str` | Active system prompt |
| `history` | `list[dict]` | Conversation history (role/content pairs) |

**Methods:**

---

**`reset_chat()`**
```python
def reset_chat(self) -> None
```
Clears `self.history` and reinitializes with the system prompt.

```python
bot.reset_chat()
# bot.history == [{"role": "system", "content": "Anda adalah Lexa..."}]
```

---

**`send_message(message)`**
```python
def send_message(self, message: str) -> str
```
Sends a message to the Groq API and returns the complete response string.

- Appends user message to history.
- Makes synchronous API call.
- Appends assistant reply to history.
- On error: pops user message (history rollback), raises `RuntimeError`.

```python
reply = bot.send_message("Apa jam operasional Anda?")
print(reply)  # "Jam operasional kami adalah..."
```

---

**`send_message_stream(message)`**
```python
def send_message_stream(self, message: str) -> Generator[str, None, None]
```
Generator that yields response tokens as they arrive (streaming mode).

- Appends user message to history.
- Opens streaming API call.
- Yields each token chunk as a string.
- After full response received, appends to history.
- On error: pops user message, raises `RuntimeError`.

```python
for chunk in bot.send_message_stream("Halo"):
    print(chunk, end="", flush=True)
print()
```

---

#### Environment Variable Handling

```python
self.api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROQ API KEY")
```

Two variable names supported:
- `GROQ_API_KEY` — standard format (recommended)
- `GROQ API KEY` — non-standard format with space (legacy support)

---

### 2.2 `main.py` — CLI Interface

Simple input/output loop with the following flow:

```
start
  │
  ├── LexaChatbot() init
  │     ├── Success → continue
  │     └── ValueError → print error, sys.exit(1)
  │
  └── while True:
        │
        ├── input("Pelanggan: ")
        │
        ├── If "keluar" or "exit" → farewell message, break
        │
        ├── If empty strip → continue (no API call)
        │
        ├── send_message_stream() → print chunks
        │
        ├── except KeyboardInterrupt → farewell, break
        │
        └── except Exception → print error, continue
```

---

### 2.3 `app.py` — Streamlit Interface

**Session State Keys:**

| Key | Type | Description |
|-----|------|-------------|
| `st.session_state.chatbot` | `LexaChatbot` | Single chatbot instance per browser session |

**Page Configuration:**
```python
st.set_page_config(
    page_title="Lexa Chatbot - CS Assistant",
    page_icon="💬",
    layout="centered"
)
```

**Rendering Flow:**
```
app.py loads
  │
  ├── Custom CSS injection
  │
  ├── Sidebar: icon, title, description, reset button
  │
  ├── Main: title, caption, divider
  │
  ├── Session init: LexaChatbot() if not in session_state
  │     ├── Success → proceed
  │     └── Error → st.error() + st.info() + st.stop()
  │
  ├── History rendering loop:
  │     for message in history:
  │       skip if role == "system"
  │       st.chat_message(role) → st.markdown(content)
  │
  └── Chat input:
        if prompt := st.chat_input(...):
          Display user bubble
          Stream response into placeholder
          Full response rendered on completion
```

---

## 3. Data Flow — Message Lifecycle

```
User types "Halo" in Streamlit
          │
          ▼
st.chat_input() captures prompt
          │
          ▼
st.chat_message("user") renders bubble
          │
          ▼
send_message_stream("Halo") called
          │
          ▼
history.append({"role": "user", "content": "Halo"})
          │
          ▼
Groq API called:
  POST https://api.groq.com/openai/v1/chat/completions
  Body: {
    "model": "openai/gpt-oss-120b",
    "messages": [
      {"role": "system", "content": "Anda adalah Lexa..."},
      {"role": "user", "content": "Halo"}
    ],
    "stream": true
  }
          │
          ▼
Groq streams response chunks
          │
          ▼
Each chunk → full_response += chunk → placeholder.markdown(full_response + "▌")
          │
          ▼
Stream ends → placeholder.markdown(full_response)  ← cursor removed
          │
          ▼
history.append({"role": "assistant", "content": full_response})
```

---

## 4. Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `groq` | ≥0.9.0 | Groq Cloud API client |
| `streamlit` | ≥1.30.0 | Web UI framework |
| `python-dotenv` | ≥1.0.0 | `.env` file loading |

> Note: No versions are pinned in `requirements.txt`. This means `pip install -r requirements.txt` will always install the latest version, which may introduce breaking changes. For production, pin versions:
```
groq==0.9.0
streamlit==1.32.0
python-dotenv==1.0.1
```

---

## 5. Known Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| No chat history persistence | History lost on refresh/restart | Implement local JSON storage |
| No user authentication | All users share same API key | Add auth layer for multi-user deployment |
| Unbounded history growth | Increasing latency and memory | Implement sliding window (see Bug-005) |
| No retry logic | Single network failure fails request | Add exponential backoff |
| No input size validation | Oversized inputs cause API errors | Add client-side validation (see Bug-002) |
| No rate limit handling | Poor UX on 429 errors | Handle `RateLimitError` specifically (see Bug-004) |

---

## 6. Extending Lexa

### Custom System Prompt

```python
custom_prompt = (
    "Anda adalah Lexa, asisten khusus untuk toko elektronik XYZ. "
    "Anda ahli dalam produk laptop, smartphone, dan aksesori. "
    "Berikan rekomendasi produk yang sesuai kebutuhan pelanggan."
)
bot = LexaChatbot(system_instruction=custom_prompt)
```

### Using a Different Model

```python
# Faster, smaller model:
bot = LexaChatbot(model="llama-3.1-8b-instant")

# Larger, more capable model:
bot = LexaChatbot(model="llama-3.3-70b-versatile")
```

Available models: [https://console.groq.com/docs/models](https://console.groq.com/docs/models)

### Non-Streaming Mode

```python
# Use send_message() instead of send_message_stream() for full response at once:
reply = bot.send_message("Halo")
print(reply)
```

---

## 7. Security Considerations

See [Security Testing Report](../tests/SecurityTesting.md) for full details.

**Critical items for developers:**
1. Always add `.env` to `.gitignore` before first commit.
2. Never hardcode the API key in source files.
3. Implement input validation before API calls.
4. Add anti-injection clauses to the system prompt for production use.
5. Pin dependency versions and audit with `pip-audit`.
