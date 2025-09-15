## NGPF Check Writing Interactive

Streamlit-based interactive to practice filling out checks using the I do → We do → You do model. No backend, no PII, no persistence beyond the browser session.

### Requirements
- Python 3.9+

### Setup
```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows (Git Bash)
# For PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Run
```bash
streamlit run app.py
```

### Embed and Deploy
- See `EMBEDDING.md` for iframe snippet and baseUrlPath configuration.
- Docker:
```bash
docker build -t check-writing .
docker run -p 8501:8501 check-writing
```

### Privacy
- No analytics or external network calls.
- All state remains in `st.session_state` and is cleared on refresh/close.

### Design
- Follow `style-guide.md` for colors, typography, and spacing.
- Global theme in `.streamlit/config.toml`; additional CSS injected in `app.py`.

### Development
- Sprint tracking in `sprint-tracker.md`.
- Core tokens in `tokens.py`.


