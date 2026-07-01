# Installation Guide — SH04-AI-Chatbot-LEXA

**Project:** SH04-AI-Chatbot-LEXA  
**Version:** 1.0.0  
**Last Updated:** 2025-07-01

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.9 | 3.11+ |
| RAM | 2 GB free | 4 GB free |
| Storage | 200 MB | 500 MB |
| OS | Windows 10 / macOS 12 / Ubuntu 20.04 | Latest stable |
| Network | Required (for Groq API) | Stable broadband |

---

## Step 1 — Get Groq API Key

1. Open [https://console.groq.com](https://console.groq.com) in your browser.
2. Sign up for a free account or log in.
3. Navigate to **API Keys** in the sidebar.
4. Click **"Create API Key"**.
5. Copy the key (starts with `gsk_...`). **Store it securely — it will not be shown again.**

> ✅ Groq offers a generous free tier with fast LPU inference.

---

## Step 2 — Get the Project Files

**Option A — Clone from Git:**
```bash
git clone https://github.com/your-repo/SH04-AI-Chatbot-LEXA.git
cd SH04-AI-Chatbot-LEXA
```

**Option B — Download ZIP:**
1. Download and extract the project ZIP.
2. Open a terminal and navigate to the extracted folder.

**Verify files exist:**
```
SH04-AI-Chatbot-LEXA/
├── main.py
├── app.py
├── llm.py
├── requirements.txt
└── README.md
```

---

## Step 3 — Set Up Python Virtual Environment

Using a virtual environment is **strongly recommended** to isolate dependencies.

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Windows (Command Prompt)
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Verify activation** — your prompt should show `(.venv)`:
```
(.venv) user@machine:~/project$
```

---

## Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `groq` — Groq Cloud API SDK
- `streamlit` — Web UI framework
- `python-dotenv` — Environment variable loader

**Verify installation:**
```bash
pip list | grep -E "groq|streamlit|python-dotenv"
```

Expected output:
```
groq                0.x.x
python-dotenv       1.x.x
streamlit           1.x.x
```

---

## Step 5 — Configure Environment Variables

Create a file named `.env` in the project root:

```bash
# On macOS/Linux:
touch .env

# On Windows (PowerShell):
New-Item .env -ItemType File
```

Open `.env` in a text editor and add:
```env
GROQ_API_KEY=gsk_YourActualGroqApiKeyHere
```

> ⚠️ **Security Warning:** Never commit this file to version control. Add `.env` to your `.gitignore`.

**Create `.gitignore` (important!):**
```bash
echo ".env" >> .gitignore
echo ".venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
```

---

## Step 6 — Verify Installation

Run a quick test to verify everything is working:

```bash
python -c "
from llm import LexaChatbot
print('Import successful')
bot = LexaChatbot()
print('Chatbot initialized successfully')
print('Model:', bot.model)
"
```

Expected output:
```
Import successful
Chatbot initialized successfully
Model: openai/gpt-oss-120b
```

If you see an error, check the Troubleshooting section below.

---

## Step 7 — Run the Application

### Option A: CLI Mode
```bash
python main.py
```

### Option B: Streamlit Web UI
```bash
streamlit run app.py
```

The browser will automatically open at `http://localhost:8501`.

---

## Troubleshooting Installation

### Error: `python` not found
```
'python' is not recognized as an internal or external command
```
**Fix:** Use `python3` instead of `python`, or ensure Python is added to PATH.

---

### Error: `pip` not found
**Fix:**
```bash
python -m pip install -r requirements.txt
```

---

### Error: `ModuleNotFoundError: No module named 'groq'`
**Fix:** Ensure your virtual environment is activated before installing:
```bash
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

---

### Error: `ValueError: API Key Groq tidak ditemukan!`
**Fix:** Ensure `.env` file exists with correct content:
```bash
cat .env
# Should output: GROQ_API_KEY=gsk_...
```

---

### Error: PowerShell execution policy (Windows)
```
cannot be loaded because running scripts is disabled on this system
```
**Fix:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Streamlit port already in use
```
Port 8501 is already in use
```
**Fix:**
```bash
streamlit run app.py --server.port 8502
```

---

## Uninstallation

To remove the project and its dependencies:
```bash
deactivate          # Exit virtual environment
cd ..
rm -rf SH04-AI-Chatbot-LEXA/   # Remove project folder
```

No system-wide changes are made when using a virtual environment.
