"""NGPF Check Writing Interactive — Sprint 1 UI

Scaffold with global styles, header, responsive container, controls, and static Check UI.
No external calls, no persistence beyond session.
"""

from __future__ import annotations

import streamlit as st
import base64
from pathlib import Path

try:
    import tokens as design_tokens
except Exception:
    # Fallbacks if tokens module is missing
    class _FallbackTokens:  # type: ignore
        ROYAL_BLUE = "#1f3b9b"
        NAVY_BLUE = "#0b1541"
        BRIGHT_BLUE = "#275ce4"
        SKY_BLUE = "#1db8e8"
        GOLD = "#f4ad00"
        ORANGE = "#f78219"
        SOFT_BLUE_TINT = "#edfaff"
        LIGHT_GRAY_BLUE = "#d2d8e9"
        ICE_BLUE = "#d2eff9"
        ERROR_RED = "#D32F2F"
        HEADLINE_FONT = "PT Sans, sans-serif"
        BODY_FONT = "Montserrat, sans-serif"

    design_tokens = _FallbackTokens()  # type: ignore


st.set_page_config(
    page_title="NGPF Check Writing",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def _get_check_bg_data_url() -> str | None:
    """Return data URL for a background image if an assets/check.* file exists (case-insensitive)."""
    assets_dir = Path("assets")
    if not assets_dir.exists():
        return None
    allowed_exts = {"png", "jpg", "jpeg", "svg", "webp"}
    # Prefer files named exactly check.* but accept case-insensitive
    candidates: list[Path] = []
    for p in assets_dir.iterdir():
        if not p.is_file():
            continue
        name_lower = p.name.lower()
        ext = p.suffix.lower().strip(".")
        if ext in allowed_exts and (name_lower == f"check.{ext}" or name_lower.startswith("check.")):
            candidates.append(p)
    # Stable order
    candidates.sort(key=lambda x: x.name.lower())
    for p in candidates:
        ext = p.suffix.lower().strip(".")
        try:
            data = p.read_bytes()
            b64 = base64.b64encode(data).decode("utf-8")
            mime = "image/svg+xml" if ext == "svg" else f"image/{ext}"
            return f"data:{mime};base64,{b64}"
        except Exception:
            continue
    return None


def inject_global_styles() -> None:
    """Inject CSS variables, fonts, focus styles, and basic layout tokens."""
    bg_data_url = _get_check_bg_data_url()
    bg_image_block = (
        f"background-image: url('{bg_data_url}'); background-size: cover; background-position: center;"
        if bg_data_url
        else ""
    )
    css = f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=PT+Sans:wght@700&family=Montserrat:wght@400;500;700&display=swap');
      :root {{
        --color-royal-blue: {design_tokens.ROYAL_BLUE};
        --color-navy-blue: {design_tokens.NAVY_BLUE};
        --color-bright-blue: {design_tokens.BRIGHT_BLUE};
        --color-sky-blue: {design_tokens.SKY_BLUE};
        --color-gold: {design_tokens.GOLD};
        --color-orange: {design_tokens.ORANGE};
        --color-soft-blue-tint: {design_tokens.SOFT_BLUE_TINT};
        --color-light-gray-blue: {design_tokens.LIGHT_GRAY_BLUE};
        --color-ice-blue: {design_tokens.ICE_BLUE};
        --color-error-red: {design_tokens.ERROR_RED};
        --spacing-sm: 8px;
        --spacing-md: 16px;
        --spacing-lg: 24px;
      }}

      /* Base typography */
      html, body, [data-testid="stAppViewContainer"] * {{
        font-family: {design_tokens.BODY_FONT};
        font-size: 18px;
        line-height: 1.4;
      }}
      h1 {{
        font-family: {design_tokens.HEADLINE_FONT};
        font-weight: 700;
        font-size: 48px;
        line-height: 1.2;
        color: var(--color-royal-blue);
        margin: 0;
      }}
      h2 {{
        font-family: {design_tokens.BODY_FONT};
        font-weight: 700;
        font-size: 36px;
        color: var(--color-royal-blue);
      }}
      h3 {{
        font-family: {design_tokens.BODY_FONT};
        font-weight: 700;
        font-size: 24px;
        color: var(--color-royal-blue);
      }}
      h4 {{
        font-family: {design_tokens.BODY_FONT};
        font-weight: 700;
        font-size: 20px;
        text-transform: uppercase;
        color: var(--color-royal-blue);
      }}
      h5 {{
        font-family: {design_tokens.BODY_FONT};
        font-weight: 700;
        font-size: 18px;
        text-transform: uppercase;
        color: var(--color-royal-blue);
      }}
      h6 {{
        font-family: {design_tokens.BODY_FONT};
        font-weight: 700;
        font-size: 16px;
        text-transform: uppercase;
        color: var(--color-royal-blue);
      }}

      /* Links */
      a, .stMarkdown a {{ color: var(--color-royal-blue); font-size: 20px; }}

      /* Focus visibility for keyboard users */
      *:focus-visible {{
        outline: 3px solid var(--color-bright-blue) !important;
        outline-offset: 2px;
        border-radius: 4px;
      }}

      /* Header */
      .ngpf-header {{
        display: flex;
        align-items: center;
        gap: var(--spacing-md);
        padding: var(--spacing-md);
        background: var(--color-soft-blue-tint);
        border-bottom: 1px solid var(--color-light-gray-blue);
      }}
      .ngpf-logo {{
        width: 48px;
        height: 48px;
        border-radius: 6px;
        background: white;
        border: 2px solid var(--color-light-gray-blue);
      }}
      .ngpf-header-title {{
        display: flex;
        flex-direction: column;
      }}
      .ngpf-subtitle {{
        font-size: 18px;
        color: var(--color-navy-blue);
      }}

      /* Main content container */
      .ngpf-container {{
        padding: var(--spacing-lg);
      }}

      /* Controls panel */
      .ngpf-controls {{
        background: #fff;
        border: 1px solid var(--color-light-gray-blue);
        border-radius: 12px;
        padding: var(--spacing-lg);
      }}
      .stButton > button {{
        font-weight: 700;
        border-radius: 6px;
        padding: 8px 16px;
      }}

      /* Tabs styling to match guide */
      .stTabs [role="tab"] {{
        background: var(--color-soft-blue-tint);
        color: var(--color-royal-blue);
        border-radius: 6px;
        padding: 8px 12px;
      }}
      .stTabs [role="tab"][aria-selected="true"] {{
        background: var(--color-bright-blue) !important;
        color: #fff !important;
      }}

      /* Check visual - realistic layout */
      .check-real {{
        position: relative;
        width: 920px;
        max-width: 100%;
        aspect-ratio: 2.2 / 1;
        background: radial-gradient(circle at 30% 40%, #f3fff8 0%, #e8f7f0 55%, #f7fffc 100%);
        {bg_image_block}
        border: 2px solid var(--color-light-gray-blue);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        overflow: hidden;
      }}
      .check-number {{
        position: absolute; right: 20px; top: 16px;
        font-weight: 700; color: var(--color-navy-blue);
        letter-spacing: 2px;
      }}
      .date-wrap {{
        position: absolute; right: 20px; top: 56px; width: 360px;
      }}
      .small-label {{
        font-weight: 700; letter-spacing: 2px; color: var(--color-navy-blue);
      }}
      .date-line {{
        border-bottom: 2px solid var(--color-light-gray-blue);
        height: 28px; border-radius: 2px;
      }}
      .check-row {{
        display: grid;
        grid-template-columns: 1fr 260px;
        gap: 12px;
        align-items: end;
        margin-bottom: 14px;
      }}
      .check-row.words {{ grid-template-columns: 1fr 100px; align-items: center; }}
      .check-row.bottom {{ grid-template-columns: 1fr 1fr; margin-top: 10px; }}
      .check-label {{
        font-weight: 600;
        color: var(--color-navy-blue);
        font-size: 14px;
        margin-bottom: 4px;
      }}
      .line {{
        border-bottom: 2px solid var(--color-light-gray-blue);
        height: 34px;
        position: relative;
        border-radius: 2px;
      }}
      .fill {{
        position: absolute;
        left: 10px;
        right: 10px;
        bottom: 4px;
        color: var(--color-navy-blue);
        font-weight: 600;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }}
      .amount-box {{
        height: 40px;
        border: 2px solid var(--color-light-gray-blue);
        border-radius: 6px;
        display: flex;
        align-items: center;
        padding: 0 10px;
        justify-content: flex-end;
        font-weight: 700;
        color: var(--color-navy-blue);
      }}
      .dollars-label {{
        color: var(--color-navy-blue);
        font-weight: 700;
        text-transform: uppercase;
        justify-self: end;
        font-size: 22px;
      }}
      .micr {{
        margin-top: 12px;
        color: var(--color-navy-blue);
        letter-spacing: 2px;
        opacity: 0.5;
        font-size: 14px;
        text-align: center;
      }}
      .hotspot {{
        position: absolute;
        display: block;
        border: 2px dashed transparent;
        border-radius: 6px;
        cursor: pointer;
      }}
      .hotspot:focus-visible, .hotspot:hover {{
        border-color: var(--color-bright-blue);
        outline: none;
        background: rgba(39,92,228,0.06);
      }}
      .field-hint {{
        color: var(--color-navy-blue);
        font-size: 14px;
        margin-top: 4px;
      }}
      .field-error {{
        color: var(--color-error-red);
        font-size: 14px;
        margin-top: 4px;
      }}
      .field-ok {{
        color: var(--color-bright-blue);
        font-size: 14px;
        margin-top: 4px;
        font-weight: 600;
      }}
      @media (max-width: 480px) {{
        .check-row {{ grid-template-columns: 1fr; }}
      }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_header() -> None:
    header_html = """
    <div class="ngpf-header" role="banner">
      <div class="ngpf-logo" aria-hidden="true"></div>
      <div class="ngpf-header-title">
        <h1>Check Writing Interactive</h1>
        <div class="ngpf-subtitle">NGPF — I do · We do · You do</div>
      </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def _ensure_session_state_defaults() -> None:
    if "selected_scenario" not in st.session_state:
        st.session_state.selected_scenario = 0
    if "mode" not in st.session_state:
        st.session_state.mode = "I do"
    if "guided_step" not in st.session_state:
        st.session_state.guided_step = -1  # -1 = before first step
    if "_last_scenario" not in st.session_state:
        st.session_state._last_scenario = st.session_state.selected_scenario
    if "_last_mode" not in st.session_state:
        st.session_state._last_mode = st.session_state.mode
    # Defaults for We do inputs
    for key, default in [
        ("we_date", ""),
        ("we_payee", ""),
        ("we_amount_numeric", ""),
        ("we_amount_words", ""),
        ("we_memo", ""),
        ("we_signature", ""),
    ]:
        st.session_state.setdefault(key, default)


def _get_scenarios() -> list[dict[str, str]]:
    return [
        {
            "title": "Plumbing Ink 123 — $150",
            "prompt": "Write a check to Plumbing Ink 123 for $150.00.",
        },
        {
            "title": "Monthly Rent — $1,200",
            "prompt": "Write a check to Oakwood Apartments for $1,200.00.",
        },
        {
            "title": "Utilities — $86.45",
            "prompt": "Write a check to City Utilities for $86.45.",
        },
        {
            "title": "Grocery Store — $64.32",
            "prompt": "Write a check to FreshMart for $64.32.",
        },
        {
            "title": "Donation — $50",
            "prompt": "Write a check to Community Fund for $50.00.",
        },
    ]


@st.cache_data(show_spinner=False)
def _get_guided_scenarios() -> list[dict]:
    """Guided step scripts for "I do" mode.

    Each scenario defines ordered steps that auto-fill the check and include explanations.
    """
    return [
        {
            "title": "Plumbing Ink 123 — $150",
            "amount_numeric": "$150.00",
            "amount_words": "One hundred fifty dollars and 00/100",
            "payee": "Plumbing Ink 123",
            "date": "10/15/2025",
            "memo": "Service call",
            "signature": "John Doe",
            "steps": [
                {
                    "field": "date",
                    "value": "10/15/2025",
                    "explanation": "Write today’s date clearly in MM/DD/YYYY format.",
                },
                {
                    "field": "payee",
                    "value": "Plumbing Ink 123",
                    "explanation": "Enter the payee’s name exactly as provided.",
                },
                {
                    "field": "amount_numeric",
                    "value": "$150.00",
                    "explanation": "Write the numeric amount including cents (use .00 if no cents).",
                },
                {
                    "field": "amount_words",
                    "value": "One hundred fifty dollars and 00/100",
                    "explanation": "Write the amount in words and include the cents as a fraction.",
                },
                {
                    "field": "memo",
                    "value": "Service call",
                    "explanation": "Memo is optional but helpful for your records.",
                },
                {
                    "field": "signature",
                    "value": "John Doe",
                    "explanation": "Sign your name as it appears on your bank account.",
                },
            ],
        },
        {
            "title": "Monthly Rent — $1,200",
            "amount_numeric": "$1,200.00",
            "amount_words": "One thousand two hundred dollars and 00/100",
            "payee": "Oakwood Apartments",
            "date": "10/01/2025",
            "memo": "October rent",
            "signature": "John Doe",
            "steps": [],  # Fallback to auto from fields if needed later
        },
        {
            "title": "Utilities — $86.45",
            "amount_numeric": "$86.45",
            "amount_words": "Eighty-six dollars and 45/100",
            "payee": "City Utilities",
            "date": "10/10/2025",
            "memo": "Account 12345",
            "signature": "John Doe",
            "steps": [],
        },
        {
            "title": "Grocery Store — $64.32",
            "amount_numeric": "$64.32",
            "amount_words": "Sixty-four dollars and 32/100",
            "payee": "FreshMart",
            "date": "10/12/2025",
            "memo": "Groceries",
            "signature": "John Doe",
            "steps": [],
        },
        {
            "title": "Donation — $50",
            "amount_numeric": "$50.00",
            "amount_words": "Fifty dollars and 00/100",
            "payee": "Community Fund",
            "date": "10/20/2025",
            "memo": "Donation",
            "signature": "John Doe",
            "steps": [],
        },
    ]


def _reset_all_state() -> None:
    for k in list(st.session_state.keys()):
        del st.session_state[k]


def _ensure_flow_defaults() -> None:
    st.session_state.setdefault("screen", "scenario")  # scenario -> i_do -> we_do -> you_do
    st.session_state.setdefault("selected_scenario", 0)
    st.session_state.setdefault("guided_step", -1)
    st.session_state.setdefault("mode", "I do")


def render_top_nav() -> None:
    with st.container():
        st.markdown('<div class="ngpf-container">', unsafe_allow_html=True)
        cols = st.columns([1, 3, 1])
        with cols[0]:
            if st.button("Reset", type="secondary"):
                _reset_all_state()
                st.rerun()
        with cols[1]:
            step_map = {"scenario": 0, "i_do": 1, "we_do": 2, "you_do": 3}
            current = step_map.get(st.session_state.screen, 0)
            st.progress(current / 3.0, text=f"Step {current}/3" if current else "Pick a scenario")
        with cols[2]:
            back_enabled = st.session_state.screen in {"we_do", "you_do"}
            if st.button("Back", disabled=not back_enabled):
                if st.session_state.screen == "we_do":
                    st.session_state.screen = "i_do"
                elif st.session_state.screen == "you_do":
                    st.session_state.screen = "we_do"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def render_scenario_screen() -> None:
    scenarios = _get_scenarios()
    with st.container():
        st.markdown('<div class="ngpf-container">', unsafe_allow_html=True)
        st.markdown("### Choose a scenario")
        rows = st.columns(3)
        for i, sc in enumerate(scenarios):
            col = rows[i % 3]
            with col:
                if st.button(sc["title"], key=f"scenario_{i}"):
                    st.session_state.selected_scenario = i
                    st.session_state.screen = "i_do"
                    st.session_state.guided_step = -1
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def render_check_static() -> None:
    scenario = _get_scenarios()[st.session_state.selected_scenario]
    with st.container():
        st.markdown('<div class="ngpf-container">', unsafe_allow_html=True)
        st.markdown("#### Scenario", help="Use this prompt to fill out the check in later sprints.")
        st.info(scenario["prompt"])

        # Static visual of a check (realistic layout)
        check_html = """
        <div class="check-real" role="group" aria-label="Check fields (static)">
          <div class="check-number">0025</div>
          <div class="date-wrap">
            <div class="small-label">DATE</div>
            <div class="date-line"></div>
          </div>
          <div class="check-row" style="margin-top: 96px;">
            <div>
              <div class="check-label">PAY TO THE ORDER OF</div>
              <div class="line"></div>
            </div>
            <div>
              <div class="check-label">$</div>
              <div class="amount-box"></div>
            </div>
          </div>
          <div class="check-row words">
            <div>
              <div class="line"></div>
            </div>
            <div class="dollars-label">DOLLARS</div>
          </div>
          <div class="check-row bottom" style="margin-top: 28px;">
            <div>
              <div class="check-label">MEMO</div>
              <div class="line"></div>
            </div>
            <div>
              <div class="check-label" style="text-align:right">AUTHORIZED SIGNATURE</div>
              <div class="line"></div>
            </div>
          </div>
          <div class="micr">||:789123456||: 123789456123&quot; 0025</div>
        </div>
        """
        st.markdown(check_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def _compute_filled_fields(scenario_idx: int, step_index: int) -> dict[str, str]:
    guided = _get_guided_scenarios()[scenario_idx]
    fields: dict[str, str] = {
        "date": "",
        "payee": "",
        "amount_words": "",
        "amount_numeric": "",
        "memo": "",
        "signature": "",
    }
    steps = guided.get("steps") or []
    if not steps:
        # If steps are not explicitly defined, fill in default order up to index
        default_order = [
            ("date", guided.get("date", "")),
            ("payee", guided.get("payee", "")),
            ("amount_numeric", guided.get("amount_numeric", "")),
            ("amount_words", guided.get("amount_words", "")),
            ("memo", guided.get("memo", "")),
            ("signature", guided.get("signature", "")),
        ]
        for i, (f, v) in enumerate(default_order):
            if i <= step_index:
                fields[f] = v
        return fields

    for i, step in enumerate(steps):
        if i <= step_index:
            fields[step["field"]] = step["value"]
    return fields


def render_check_guided() -> None:
    scenario_idx = st.session_state.selected_scenario
    guided = _get_guided_scenarios()[scenario_idx]
    steps = guided.get("steps") or [
        {"field": "date", "value": guided.get("date", ""), "explanation": "Date"},
        {"field": "payee", "value": guided.get("payee", ""), "explanation": "Payee"},
        {
            "field": "amount_numeric",
            "value": guided.get("amount_numeric", ""),
            "explanation": "Numeric amount",
        },
        {
            "field": "amount_words",
            "value": guided.get("amount_words", ""),
            "explanation": "Amount in words",
        },
        {"field": "memo", "value": guided.get("memo", ""), "explanation": "Memo"},
        {
            "field": "signature",
            "value": guided.get("signature", ""),
            "explanation": "Signature",
        },
    ]

    total_steps = len(steps)
    current = st.session_state.guided_step
    current_clamped = max(-1, min(current, total_steps - 1))
    fields = _compute_filled_fields(scenario_idx, current_clamped)

    with st.container():
        st.markdown('<div class="ngpf-container">', unsafe_allow_html=True)
        st.markdown("#### I do — Guided walkthrough")

        # Progress info
        progress_ratio = 0.0 if current_clamped < 0 else (current_clamped + 1) / total_steps
        st.progress(progress_ratio, text=f"Step {max(0, current_clamped + 1)} of {total_steps}")

        # Check with filled fields (realistic layout)
        check_html = f"""
        <div class=\"check-real\" role=\"group\" aria-label=\"Check fields (guided)\"> 
          <div class=\"check-number\">0025</div>
          <button class=\"hotspot\" style=\"right:20px; top:56px; width:360px; height:42px\" aria-label=\"Date field\"></button>
          <div class=\"date-wrap\">
            <div class=\"small-label\">DATE</div>
            <div class=\"date-line\"></div>
          </div>

          <button class=\"hotspot\" style=\"left:20px; top:96px; width: calc(100% - 320px); height:58px\" aria-label=\"Pay to the Order of field\"></button>
          <button class=\"hotspot\" style=\"right:20px; top:110px; width:220px; height:42px\" aria-label=\"Numeric amount field\"></button>

          <button class=\"hotspot\" style=\"left:20px; top:166px; width: calc(100% - 240px); height:58px\" aria-label=\"Amount in words field\"></button>

          <button class=\"hotspot\" style=\"left:20px; bottom:74px; width:45%; height:42px\" aria-label=\"Memo field\"></button>
          <button class=\"hotspot\" style=\"right:20px; bottom:74px; width:45%; height:42px\" aria-label=\"Signature field\"></button>

          <div class=\"check-row\" style=\"margin-top: 96px;\"> 
            <div>
              <div class=\"check-label\">PAY TO THE ORDER OF</div>
              <div class=\"line\"><div class=\"fill\">{fields['payee']}</div></div>
            </div>
            <div>
              <div class=\"check-label\">$</div>
              <div class=\"amount-box\">{fields['amount_numeric']}</div>
            </div>
          </div>
          <div class=\"check-row words\">
            <div>
              <div class=\"line\"><div class=\"fill\">{fields['amount_words']}</div></div>
            </div>
            <div class=\"dollars-label\">DOLLARS</div>
          </div>
          <div class=\"check-row bottom\" style=\"margin-top: 28px;\">
            <div>
              <div class=\"check-label\">MEMO</div>
              <div class=\"line\"><div class=\"fill\">{fields['memo']}</div></div>
            </div>
            <div>
              <div class=\"check-label\" style=\"text-align:right\">AUTHORIZED SIGNATURE</div>
              <div class=\"line\"><div class=\"fill\">{fields['signature']}</div></div>
            </div>
          </div>
          <div class=\"micr\">||:789123456||: 123789456123\" 0025</div>
        </div>
        """
        st.markdown(check_html, unsafe_allow_html=True)

        # Explanation for current step
        if current_clamped >= 0:
            st.info(steps[current_clamped]["explanation"])
        else:
            st.caption("Click Next to begin the guided walkthrough.")

        cols = st.columns([1, 1, 4])
        with cols[0]:
            if st.button("Next", type="primary", disabled=current_clamped >= total_steps - 1):
                st.session_state.guided_step = min(current_clamped + 1, total_steps - 1)
                st.rerun()
        with cols[1]:
            if st.button("Replay", type="secondary"):
                st.session_state.guided_step = -1
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


def _normalize_text(value: str) -> str:
    return " ".join(value.strip().lower().split())


def _parse_currency(value: str) -> float | None:
    try:
        cleaned = value.replace("$", "").replace(",", "").strip()
        return float(cleaned)
    except Exception:
        return None


def _validate_date(value: str) -> tuple[bool, str | None]:
    from datetime import datetime

    formats = ["%m/%d/%Y", "%m/%d/%y", "%m-%d-%Y", "%m-%d-%y"]
    for fmt in formats:
        try:
            datetime.strptime(value.strip(), fmt)
            return True, None
        except Exception:
            pass
    return False, "Use a valid date like 10/15/2025."


def _validate_payee(value: str, expected: str) -> tuple[bool, str | None]:
    if _normalize_text(value) == _normalize_text(expected):
        return True, None
    return False, f"Expected: {expected}"


def _validate_amount_numeric(value: str, expected: str) -> tuple[bool, str | None]:
    target = _parse_currency(expected)
    got = _parse_currency(value)
    if target is not None and got is not None and abs(target - got) < 0.005:
        return True, None
    return False, f"Expected: {expected}"


def _validate_amount_words(value: str, expected: str) -> tuple[bool, str | None]:
    if _normalize_text(value) == _normalize_text(expected):
        return True, None
    return False, f"Example: {expected}"


def render_check_we_do() -> None:
    scenario_idx = st.session_state.selected_scenario
    guided = _get_guided_scenarios()[scenario_idx]
    expected = {
        "date": guided.get("date", ""),
        "payee": guided.get("payee", ""),
        "amount_numeric": guided.get("amount_numeric", ""),
        "amount_words": guided.get("amount_words", ""),
        "memo": guided.get("memo", ""),
        "signature": guided.get("signature", ""),
    }

    with st.container():
        st.markdown('<div class="ngpf-container">', unsafe_allow_html=True)
        st.markdown("#### We do — Semi-guided practice")
        st.caption("Type into each field. Corrections will appear below as you go.")

        # Date
        st.text_input("Date (MM/DD/YYYY) (required)", key="we_date", placeholder="10/15/2025")
        ok, msg = _validate_date(st.session_state.we_date) if st.session_state.we_date else (False, None)
        if st.session_state.we_date:
            st.markdown(
                f"<div role='status' aria-live='polite' class='{'field-ok' if ok else 'field-error'}'>{'Looks good' if ok else msg}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown("<div class='field-hint'>Enter today’s date.</div>", unsafe_allow_html=True)

        # Payee
        st.text_input("Pay to the Order of (required)", key="we_payee", placeholder=expected["payee"])
        if st.session_state.we_payee:
            ok, msg = _validate_payee(st.session_state.we_payee, expected["payee"])
            st.markdown(
                f"<div role='status' aria-live='polite' class='{'field-ok' if ok else 'field-error'}'>{'Correct' if ok else msg}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown("<div class='field-hint'>Type the payee name exactly.</div>", unsafe_allow_html=True)

        # Amount numeric
        st.text_input("$ Amount (numeric) (required)", key="we_amount_numeric", placeholder=expected["amount_numeric"]) 
        if st.session_state.we_amount_numeric:
            ok, msg = _validate_amount_numeric(st.session_state.we_amount_numeric, expected["amount_numeric"])
            st.markdown(
                f"<div role='status' aria-live='polite' class='{'field-ok' if ok else 'field-error'}'>{'Correct' if ok else msg}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown("<div class='field-hint'>Include dollars and cents (e.g., 150.00).</div>", unsafe_allow_html=True)

        # Amount in words
        st.text_input("Amount in Words (required)", key="we_amount_words", placeholder=expected["amount_words"]) 
        if st.session_state.we_amount_words:
            ok, msg = _validate_amount_words(st.session_state.we_amount_words, expected["amount_words"])
            st.markdown(
                f"<div role='status' aria-live='polite' class='{'field-ok' if ok else 'field-error'}'>{'Correct' if ok else msg}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown("<div class='field-hint'>Use words and cents as a fraction (xx/100).</div>", unsafe_allow_html=True)

        # Memo (optional)
        st.text_input("Memo (optional)", key="we_memo", placeholder=expected["memo"])
        if st.session_state.we_memo:
            st.markdown("<div class='field-ok'>Not required, but helpful.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='field-hint'>Add a short note for your records.</div>", unsafe_allow_html=True)

        # Signature
        st.text_input("Signature", key="we_signature", placeholder="Your full name")
        if st.session_state.we_signature:
            st.markdown("<div class='field-ok'>Looks good</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='field-hint'>Sign your name as on your bank account.</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


def render_check_you_do() -> None:
    scenario_idx = st.session_state.selected_scenario
    guided = _get_guided_scenarios()[scenario_idx]
    expected = {
        "date": guided.get("date", ""),
        "payee": guided.get("payee", ""),
        "amount_numeric": guided.get("amount_numeric", ""),
        "amount_words": guided.get("amount_words", ""),
        "memo": guided.get("memo", ""),
        "signature": guided.get("signature", ""),
    }

    # Keep separate state keys for You do so We do inputs are preserved when switching tabs
    for key in [
        "you_date",
        "you_payee",
        "you_amount_numeric",
        "you_amount_words",
        "you_memo",
        "you_signature",
    ]:
        st.session_state.setdefault(key, "")

    with st.container():
        st.markdown('<div class="ngpf-container">', unsafe_allow_html=True)
        st.markdown("#### You do — Independent practice")

        scenario = _get_scenarios()[scenario_idx]
        st.info(scenario["prompt"])  # Minimal prompting per requirements

        st.text_input("Date (MM/DD/YYYY) (required)", key="you_date")
        st.text_input("Pay to the Order of (required)", key="you_payee")
        st.text_input("$ Amount (numeric) (required)", key="you_amount_numeric")
        st.text_input("Amount in Words (required)", key="you_amount_words")
        st.text_input("Memo (optional)", key="you_memo")
        st.text_input("Signature", key="you_signature")

        cols = st.columns([1, 1, 6])
        show_summary = False
        with cols[0]:
            if st.button("Check my work", type="primary"):
                show_summary = True
        with cols[1]:
            if st.button("Clear", type="secondary"):
                for k in [
                    "you_date",
                    "you_payee",
                    "you_amount_numeric",
                    "you_amount_words",
                    "you_memo",
                    "you_signature",
                ]:
                    st.session_state[k] = ""
                st.rerun()

        if show_summary:
            checks = {
                "Date": _validate_date(st.session_state.you_date),
                "Payee": _validate_payee(st.session_state.you_payee, expected["payee"]),
                "$ Amount": _validate_amount_numeric(st.session_state.you_amount_numeric, expected["amount_numeric"]),
                "Amount in Words": _validate_amount_words(st.session_state.you_amount_words, expected["amount_words"]),
            }
            st.markdown("### Results")
            all_ok = True
            for label, (ok, msg) in checks.items():
                if ok:
                    st.markdown(f"- ✅ {label}: Correct")
                else:
                    st.markdown(f"- ❌ {label}: {msg}")
                    all_ok = False
            # Memo and signature lightweight checks
            if st.session_state.you_signature.strip():
                st.markdown("- ✅ Signature: Present")
            else:
                st.markdown("- ⚠️ Signature: Add your name")
                all_ok = False
            if st.session_state.you_memo.strip():
                st.markdown("- ℹ️ Memo: Not required, but helpful")

            if all_ok:
                st.success("Great job! Everything looks correct.")
            else:
                st.info("Review the items marked above and try again.")

        st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    inject_global_styles()
    _ensure_session_state_defaults()
    _ensure_flow_defaults()
    render_header()
    render_top_nav()

    screen = st.session_state.screen
    if screen == "scenario":
        render_scenario_screen()
    elif screen == "i_do":
        # auto-fill walkthrough
        st.session_state.mode = "I do"
        render_check_guided()
        cols = st.columns([1, 1, 6])
        with cols[0]:
            if st.button("Next: We do", type="primary"):
                st.session_state.screen = "we_do"
                st.rerun()
    elif screen == "we_do":
        st.session_state.mode = "We do"
        render_check_we_do()
        cols = st.columns([1, 1, 6])
        with cols[0]:
            if st.button("Next: You do", type="primary"):
                st.session_state.screen = "you_do"
                st.rerun()
    elif screen == "you_do":
        st.session_state.mode = "You do"
        render_check_you_do()
        cols = st.columns([1, 1, 6])
        with cols[0]:
            if st.button("Finish", type="primary"):
                st.session_state.screen = "scenario"
                st.rerun()


if __name__ == "__main__":
    main()


