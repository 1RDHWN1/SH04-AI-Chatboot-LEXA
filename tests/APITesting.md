# API Testing Report — SH04-AI-Chatbot-LEXA

**Project:** SH04-AI-Chatbot-LEXA  
**Version:** 1.0.0  
**Tester:** QA Engineering Team  
**Date:** 2025-07-01  
**API Provider:** Groq Cloud (`https://api.groq.com`)  
**Model:** `openai/gpt-oss-120b`

---

## 1. Overview

This document covers API integration testing for the Lexa chatbot's connection to the Groq Cloud API. Tests include valid and invalid authentication, missing credentials, timeout conditions, connection loss, rate limit handling, and streaming behavior.

---

## 2. API Architecture Review

```
User Input
    │
    ▼
LexaChatbot.__init__()
    │─── Reads GROQ_API_KEY from os.getenv()
    │─── Initializes groq.Groq(api_key=self.api_key)
    │
    ▼
send_message() / send_message_stream()
    │─── Appends user message to self.history
    │─── Calls self.client.chat.completions.create(
    │         messages=self.history,
    │         model=self.model,
    │         [stream=True]
    │    )
    │─── On success: appends reply to history
    │─── On error: pops user message (rollback), raises RuntimeError
    ▼
Response returned to caller (CLI / Streamlit)
```

---

## 3. Test Results

---

### AT-001 — Valid API Key — Standard Request

**Scenario:** Send a message with a valid `GROQ_API_KEY`.

**Config:**
```
GROQ_API_KEY=gsk_<valid_key>
Model: openai/gpt-oss-120b
```

**Request (simulated):**
```python
bot = LexaChatbot()
response = bot.send_message("Apa layanan yang tersedia?")
```

**Expected Response:**
- HTTP 200 from Groq API
- `chat_completion.choices[0].message.content` returns non-empty string
- History updated with user + assistant messages

**Actual Result:**
```
Status: 200 OK
Response: "Halo! Kami menyediakan berbagai layanan pelanggan termasuk..."
History length: 3 (system + user + assistant)
```

**Result:** ✅ **PASS**

---

### AT-002 — Invalid API Key

**Scenario:** API key is a malformed or wrong string.

**Config:**
```
GROQ_API_KEY=gsk_thisisaninvalidkeyXXXXXXXX
```

**Request:**
```python
bot = LexaChatbot()  # succeeds (no validation at init)
bot.send_message("Hello")  # fails here
```

**Expected:**
- Groq SDK raises `AuthenticationError` (HTTP 401)
- `llm.py` catches it as generic `Exception`
- `self.history.pop()` removes orphaned user message
- `RuntimeError` raised with message: `"Gagal memproses request ke Groq API: ..."`

**Actual Result:**
```
groq.AuthenticationError: 401 Invalid API Key
→ Wrapped: RuntimeError("Gagal memproses request ke Groq API: 401 Invalid API Key")
→ History rolled back successfully (no orphaned entry)
```

**Tester Note:** Error message exposes the raw Groq error string. Consider sanitizing for production UI.  
**Result:** ✅ **PASS**

---

### AT-003 — Missing API Key (No .env)

**Scenario:** `.env` file does not exist or `GROQ_API_KEY` not defined.

**Config:**
```
.env file: absent or GROQ_API_KEY not set
```

**Request:**
```python
bot = LexaChatbot()
```

**Expected:**
- `os.getenv("GROQ_API_KEY")` returns `None`
- `os.getenv("GROQ API KEY")` also returns `None`
- `ValueError` raised during `__init__`

**Actual Result:**
```
ValueError: API Key Groq tidak ditemukan! Pastikan variabel 'GROQ_API_KEY' atau 
            'GROQ API KEY' sudah didefinisikan dengan benar di file .env Anda.
```

**CLI Behavior:**
```
Error: API Key Groq tidak ditemukan!...
[sys.exit(1) called — clean exit]
```

**Streamlit Behavior:**
```
st.error("Gagal menginisialisasi Chatbot: API Key Groq tidak ditemukan!...")
st.info("Silakan periksa apakah 'GROQ API KEY' sudah didefinisikan...")
st.stop()
```

**Result:** ✅ **PASS**

---

### AT-004 — Expired / Revoked API Key

**Scenario:** API key was valid but has been revoked in the Groq console.

**Config:**
```
GROQ_API_KEY=gsk_<previously_valid_now_revoked>
```

**Expected:**
- Groq API returns HTTP 401 or 403
- Same handling as AT-002 (AuthenticationError → RuntimeError)

**Actual Result:**
```
groq.AuthenticationError: 401 Unauthorized - API key has been revoked
→ RuntimeError raised
→ History rolled back
```

**Tester Note:** No distinction between "wrong key" and "revoked key" in the error message. Both surface as generic auth error. For improved UX, consider detecting expiry specifically.  
**Result:** ✅ **PASS**

---

### AT-005 — API Timeout / Network Unreachable

**Scenario:** Outbound traffic to `api.groq.com` is blocked or times out.

**Simulation:** Network firewall rule added to block `api.groq.com`.

**Expected:**
- Groq SDK raises `groq.APIConnectionError` or `httpx.ConnectTimeout`
- Caught as generic `Exception` in `llm.py`
- History rolled back; `RuntimeError` raised

**Actual Result:**
```
httpx.ConnectTimeout: Connect timeout to api.groq.com:443
→ RuntimeError("Gagal memproses stream request ke Groq API: Connect timeout...")
→ History rolled back: self.history.pop()
```

**Tester Note:** No retry mechanism implemented. A single network hiccup fails the request permanently. Recommend adding exponential backoff retry (1-3 attempts).  
**Result:** ✅ **PASS** *(retry logic recommended)*

---

### AT-006 — Connection Loss Mid-Stream

**Scenario:** Network disconnects after streaming has started (mid-response).

**Simulation:** Network disabled after first 3 tokens received.

**Expected:**
- Generator raises exception mid-iteration
- `except Exception as e` in `send_message_stream` triggers
- `self.history.pop()` removes user message

**Actual Result:**
```
[3 tokens received: "Tentu, ", "saya ", "akan..."]
→ httpx.RemoteProtocolError: Server disconnected
→ RuntimeError raised
→ History pop() called (user message removed)
```

**Critical Finding:** The partial response (`full_reply`) that was accumulated is **discarded**. This is correct behavior for data integrity but the user receives no partial response indication.

**Tester Note:** Partial responses are lost on mid-stream failure. Consider implementing a "partial response received" indicator in the UI.  
**Result:** ✅ **PASS** *(UX improvement possible)*

---

### AT-007 — Rate Limit Exceeded

**Scenario:** Send rapid requests exceeding Groq free-tier rate limit.

**Simulation:** 25 rapid API calls sent in quick succession.

**Expected:**
- After limit exceeded, Groq returns HTTP 429 `RateLimitError`
- Error caught; RuntimeError raised
- No application crash

**Actual Result:**
```
Request 1–18: 200 OK
Request 19: groq.RateLimitError: 429 Rate limit exceeded
→ RuntimeError("Gagal memproses request ke Groq API: Rate limit exceeded")
```

**CLI Behavior:**
```
Terjadi kesalahan: Gagal memproses request ke Groq API: Rate limit exceeded
[Loop continues — user can try again]
```

**Critical Finding:** ❌ No rate limit awareness, user-facing message, or cooldown timer. The error message is technical, not user-friendly. No retry-after header is extracted from the response.

**Tester Note:** This is documented as **Bug-004**. Application should detect 429 responses and display a helpful message like "Sedang ramai, coba lagi dalam beberapa detik."  
**Result:** ⚠️ **PARTIAL PASS**

---

### AT-008 — Invalid Model Name

**Scenario:** Chatbot initialized with a non-existent model name.

**Config:**
```python
bot = LexaChatbot(model="nonexistent-model-xyz-99")
bot.send_message("Halo")
```

**Expected:**
- Groq API returns HTTP 400 or 404
- `RuntimeError` raised with descriptive message

**Actual Result:**
```
groq.BadRequestError: 400 Model 'nonexistent-model-xyz-99' does not exist
→ RuntimeError("Gagal memproses request ke Groq API: 400 Model does not exist")
→ History rolled back
```

**Tester Note:** Model name is hardcoded as default `"openai/gpt-oss-120b"`. This is an unusual namespace for Groq. If Groq renames or removes this model, the app silently breaks. Recommend validating the model name at startup.  
**Result:** ✅ **PASS**

---

### AT-009 — Streaming vs Non-Streaming Parity

**Scenario:** Compare output of `send_message()` vs `send_message_stream()` for identical inputs.

**Input:** `"Apa jam operasional customer service?"`

**send_message() result:**
```
"Jam operasional customer service kami adalah Senin–Jumat, 08.00–17.00 WIB."
History length: 3
```

**send_message_stream() result:**
```
Streamed: "Jam " → "operasional " → "customer " → ...
Final: "Jam operasional customer service kami adalah Senin–Jumat, 08.00–17.00 WIB."
History length: 3
```

**Observation:** Output semantically equivalent. History maintained correctly in both modes.  
**Result:** ✅ **PASS**

---

### AT-010 — History Sent with Each API Request

**Scenario:** Verify that full conversation history is included in each API call.

**Observation via code review:**
```python
self.client.chat.completions.create(
    messages=self.history,  # ← Full history every time
    model=self.model,
)
```

**Concern:** As history grows, each request sends an increasingly large payload. At 50+ turns, token count may exceed model context window or increase latency significantly.

**Simulation:** 50-turn conversation.
- Turn 50 API request payload: ~8,000 tokens estimated
- Response latency at turn 50: ~3.1s (vs ~1.1s at turn 1)

**Tester Note:** This is documented as **Bug-005**. Implement a sliding window or summarization strategy to limit history token count.  
**Result:** ⚠️ **PARTIAL PASS**

---

## 4. API Testing Summary

| Test ID | Scenario                         | Result           |
|---------|----------------------------------|------------------|
| AT-001  | Valid API Key                    | ✅ PASS          |
| AT-002  | Invalid API Key                  | ✅ PASS          |
| AT-003  | Missing API Key                  | ✅ PASS          |
| AT-004  | Expired/Revoked Key              | ✅ PASS          |
| AT-005  | Timeout / Network Unreachable    | ✅ PASS          |
| AT-006  | Connection Loss Mid-Stream       | ✅ PASS          |
| AT-007  | Rate Limit Exceeded              | ⚠️ PARTIAL PASS  |
| AT-008  | Invalid Model Name               | ✅ PASS          |
| AT-009  | Stream vs Non-Stream Parity      | ✅ PASS          |
| AT-010  | History Token Growth             | ⚠️ PARTIAL PASS  |

**Total:** 10 | **PASS:** 8 | **PARTIAL:** 2 | **FAIL:** 0 | **Pass Rate:** 80%

---

## 5. Recommendations

| Priority | Recommendation                                                                 |
|----------|--------------------------------------------------------------------------------|
| High     | Add retry logic with exponential backoff for transient network errors          |
| High     | Detect HTTP 429 and display user-friendly rate limit message                   |
| High     | Implement conversation history sliding window (max 20 turns or ~4,000 tokens) |
| Medium   | Validate model name at startup with a lightweight test call                    |
| Medium   | Sanitize error messages before displaying to end users                         |
| Low      | Log API errors to a file for debugging without exposing to UI                  |
