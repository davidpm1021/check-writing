Product Requirements Prompt (PRP)
Overview

A lightweight, browser-based interactive that teaches high school students how to correctly fill out checks. The tool uses the I do → We do → You do instructional model, providing a guided walkthrough, semi-guided practice, and independent practice with immediate inline feedback. It is designed for use within NGPF’s personal finance curriculum, with no data collection, no logins, and no persistence beyond the browser session.

User Flow

Open interactive inside NGPF lesson.

I do: Guided walkthrough scenario where the check auto-fills step by step with explanations.

We do: Semi-guided scenario where students type into fields with prompts and hints. Inline correction appears as they go.

You do: Independent practice. Students receive only the scenario prompt (e.g., “Write a check for $150 to Plumbing Ink 123”) and must fill in the entire check. Inline correction is provided per field.

Reset/Replay: Students can clear and restart at any time.

Closing or refreshing the browser clears all data.

Target Users

Audience: U.S. high school students in personal finance classrooms.

Use Case: Embedded in NGPF lessons as a simple interactive to practice check writing.

Constraints: Must respect extreme privacy — no accounts, no collection of student PII, no persistence after tab/window closes.

Must-Have Features

I do: Guided scenario with automatic step-by-step fill.

We do: Semi-guided with prompts, hints, and inline correction.

You do: Independent practice with inline correction.

Multiple Scenarios: 3–5 built-in examples.

Reset/Replay Button: Restart at any time.

Accessibility-first design: Keyboard input, projector-friendly, clear instructions.

Extreme Privacy: No login, no PII, no persistence after tab closure.

Technical Stack

Frontend: Streamlit (packaged for web embedding).

Backend: None (fully client-side execution).

Database: None (all state stored in st.session_state and cleared on refresh).

Auth: None.

File Structure: app.py with modular components for instructional steps.

Key Streamlit Features

st.session_state (track inputs across fields).

st.form() (structure guided vs practice modes).

st.progress() (optional, to show scenario step completion).

st.cache_data() (cache built-in scenarios for efficiency).

Integrations

None. (All logic and scenarios built in; no external APIs.)

Design

Must follow NGPF Style-Guide.md for all styling (colors, fonts, spacing).

Minimalist, classroom-friendly layout.

Inline correction: highlight errors in red, correct version shown beneath.

Projector-friendly contrast.

Responsive so it works on laptops, tablets, and smartboards.

Deployment

Build as a static, embeddable front-end module.

Delivered as a packaged Streamlit app build for embedding on the NGPF website.

No server, no environment variables, no persistent DB.

Advanced Features

None — only the core I/We/You flow with inline correction.

Benefits of Stack Choice

Streamlit: Fast prototyping, easy interactive UI, embeddable into NGPF website.

No backend / no DB: Meets strict privacy standards; nothing stored beyond browser session.

Local state only: Fully anonymous, resets on refresh, safe for classrooms.

Example User Experience

Student opens the interactive in the NGPF lesson.

Sees the first scenario: “John pays Plumbing Ink 123 for $150.”

I do: Check auto-fills line by line, explaining each step.

We do: Student types “Plumbing Ink 123” in payee → inline correction confirms correctness. They type “One hundred fifty dollars” in words → inline correction highlights formatting.

You do: Student fills the entire check independently. Errors flagged inline, corrections displayed.

Student clicks Reset to start again or switch scenarios.

Closing the tab clears all inputs; no history is saved.