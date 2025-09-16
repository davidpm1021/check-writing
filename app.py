"""NGPF Check Writing Interactive — Sprint 1 UI

Scaffold with global styles, header, responsive container, controls, and static Check UI.
No external calls, no persistence beyond session.
"""

from __future__ import annotations

import streamlit as st
import base64
from pathlib import Path
import json
import streamlit.components.v1 as components

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


def _get_logo_data_url() -> str | None:
    """Return data URL for a header logo if assets/logo.* exists (case-insensitive)."""
    assets_dir = Path("assets")
    if not assets_dir.exists():
        return None
    exts = {"png", "jpg", "jpeg", "svg", "webp"}
    candidates = []
    for p in assets_dir.iterdir():
        if p.is_file():
            name = p.name.lower()
            ext = p.suffix.lower().strip(".")
            if ext in exts and (name == f"logo.{ext}" or name.startswith("logo.")):
                candidates.append(p)
    candidates.sort(key=lambda x: x.name.lower())
    for p in candidates:
        try:
            data = p.read_bytes()
            b64 = base64.b64encode(data).decode("utf-8")
            mime = "image/svg+xml" if p.suffix.lower() == ".svg" else f"image/{p.suffix.lower().strip('.')}"
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
      @import url('https://fonts.googleapis.com/css2?family=PT+Sans:wght@700&family=Montserrat:wght@400;500;700&family=Dancing+Script:wght@700&display=swap');
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
        gap: 16px;
        padding: 24px 32px;
        background: #ffffff;
        border-bottom: 1px solid var(--color-light-gray-blue);
      }}
      .ngpf-logo {{
        width: 96px;
        height: 96px;
        border-radius: 8px;
        background: #ffffff;
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
        border: 1px solid var(--color-light-gray-blue);
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
        padding: 24px;
        max-width: 980px;
        margin: 16px auto;
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.06);
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
        overflow: visible;
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
      .signature-text {{
        font-family: 'Dancing Script', cursive;
        font-weight: 700;
        font-size: 28px;
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
      .tip {{
        position: absolute;
        background: #fff8c4;
        border: 1px solid var(--color-light-gray-blue);
        border-radius: 8px;
        padding: 6px 12px;
        color: var(--color-navy-blue);
        font-size: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        max-width: 80%;
        min-width: 40%;
        z-index: 3;
      }}
      /* Arrow for tip appearing below the field (pointing up) */
      .tip.below::before {{
        content: '';
        position: absolute;
        top: -8px;
        left: 20px;
        border-width: 8px;
        border-style: solid;
        border-color: transparent transparent #fff8c4 transparent;
      }}
      .tip.below::after {{
        content: '';
        position: absolute;
        top: -9px;
        left: 20px;
        border-width: 9px;
        border-style: solid;
        border-color: transparent transparent var(--color-light-gray-blue) transparent;
      }}
      /* Arrow for tip appearing above the field (pointing down) */
      .tip.above::before {{
        content: '';
        position: absolute;
        bottom: -8px;
        left: 20px;
        border-width: 8px;
        border-style: solid;
        border-color: #fff8c4 transparent transparent transparent;
      }}
      .tip.above::after {{
        content: '';
        position: absolute;
        bottom: -9px;
        left: 20px;
        border-width: 9px;
        border-style: solid;
        border-color: var(--color-light-gray-blue) transparent transparent transparent;
      }}
      .cal-box {{
        position: absolute;
        border: 2px dashed var(--color-bright-blue);
        border-radius: 6px;
        background: rgba(39,92,228,0.08);
        color: var(--color-navy-blue);
        font-weight: 700;
        display: flex; align-items: center; justify-content: center;
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


def _check_overlay_component(*args, **kwargs):
    # Removed custom component usage for reliability
    raise RuntimeError("custom component disabled")


def render_header() -> None:
    logo_url = _get_logo_data_url()
    logo_style = (
        f"background-image:url('{logo_url}'); background-size: contain; background-position:center; background-repeat:no-repeat;"
        if logo_url
        else ""
    )
    header_html = f"""
    <div class=\"ngpf-header\" role=\"banner\">
      <div class=\"ngpf-logo\" aria-hidden=\"true\" style=\"{logo_style}\"></div>
      <div class=\"ngpf-header-title\">
        <h1>Check Writing Interactive</h1>
        
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
            "title": "Plumbing Inc — $150",
            "prompt": "Write a check to Plumbing Inc for $150.00.",
        },
        {
            "title": "Monthly Rent — $1,200",
            "prompt": "On November 1, 2025, write a check to Oakwood Apartments for $1,200.00 for November rent. Sign as Jordan Patel.",
        },
        {
            "title": "Field Trip Donation — $86.45",
            "prompt": "Write a check to Lincoln High PTA for $86.45 to cover a field trip fee.",
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
            "title": "Plumbing Inc — $150",
            "context": (
                "Scenario (Feb 12, 2025): Avery Thompson hired Plumbing Inc to fix a leaking kitchen faucet. "
                "The service was completed today and the invoice total is $150.00. Avery will write a check "
                "to pay the plumber before the technician leaves."
            ),
            "amount_numeric": "$150.00",
            "amount_words": "One hundred fifty dollars and 00/100",
            "payee": "Plumbing Inc",
            "date": "02/12/2025",
            "memo": "Service call",
            "signature": "Avery Thompson",
            "steps": [
                {
                    "field": "date",
                    "value": "02/12/2025",
                    "explanation": "Write today’s date clearly in MM/DD/YYYY format.",
                },
                {
                    "field": "payee",
                    "value": "Plumbing Inc",
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
                    "value": "Avery Thompson",
                    "explanation": "Sign your name as it appears on your bank account.",
                },
            ],
        },
        {
            "title": "Monthly Rent — $1,200",
            "context": (
                "Scenario (Nov 1, 2025): Jordan Patel is paying November rent to Oakwood Apartments. "
                "The amount due is $1,200.00. Jordan will write and sign a check today."
            ),
            "amount_numeric": "$1,200.00",
            "amount_words": "One thousand two hundred dollars and 00/100",
            "payee": "Oakwood Apartments",
            "date": "11/01/2025",
            "memo": "November rent",
            "signature": "Jordan Patel",
            "steps": [
                {"field": "date", "value": "11/01/2025", "explanation": "Rent is due on the 1st of the month."},
                {"field": "payee", "value": "Oakwood Apartments", "explanation": "Enter the apartment name exactly."},
                {"field": "amount_numeric", "value": "$1,200.00", "explanation": "Write the full amount with .00 cents."},
                {"field": "amount_words", "value": "One thousand two hundred dollars and 00/100", "explanation": "Write the amount in words with the cents fraction."},
                {"field": "memo", "value": "November rent", "explanation": "Memo helps you remember the purpose."},
                {"field": "signature", "value": "Jordan Patel", "explanation": "Sign your full name to authorize payment."},
            ],
        },
        {
            "title": "Field Trip Donation — $86.45",
            "context": (
                "Scenario: John donates to the school PTA to cover a field trip fee for a relative."
            ),
            "amount_numeric": "$86.45",
            "amount_words": "Eighty-six dollars and 45/100",
            "payee": "Lincoln High PTA",
            "date": "10/20/2025",
            "memo": "Field trip fee",
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
    st.session_state.setdefault("screen", "i_do")  # i_do -> we_do -> you_do
    st.session_state.setdefault("selected_scenario", 0)
    st.session_state.setdefault("guided_step", -1)
    st.session_state.setdefault("we_step", 0)
    st.session_state.setdefault("mode", "I do")
    # default overlay positions if no assets/overlay.json
    st.session_state.setdefault("overlay_positions", {
        "date": {"top": 13, "left": 62, "width": 32, "height": 7},
        "payee": {"top": 30, "left": 8, "width": 70, "height": 8},
        "amount_numeric": {"top": 30, "left": 80, "width": 12, "height": 7},
        "amount_words": {"top": 45, "left": 7, "width": 82, "height": 8},
        "memo": {"top": 72, "left": 7, "width": 42, "height": 7},
        "signature": {"top": 72, "left": 55, "width": 36, "height": 7},
    })


def _load_overlay_positions() -> dict:
    try:
        p = Path("assets/overlay.json")
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            return data
    except Exception:
        pass
    return st.session_state.get("overlay_positions", {})


def _save_overlay_positions(data: dict) -> None:
    assets_dir = Path("assets")
    assets_dir.mkdir(parents=True, exist_ok=True)
    Path("assets/overlay.json").write_text(json.dumps(data, indent=2), encoding="utf-8")


def render_top_nav() -> None:
    with st.container():
        st.markdown('<div class="ngpf-container">', unsafe_allow_html=True)
        cols = st.columns([1, 3, 1])
        with cols[0]:
            if st.button("Reset", type="secondary"):
                _reset_all_state()
                st.rerun()
        with cols[1]:
            step_map = {"i_do": 1, "we_do": 2, "you_do": 3}
            current = step_map.get(st.session_state.screen, 1)
            st.progress(current / 3.0, text=f"Step {current}/3")
        with cols[2]:
            back_enabled = st.session_state.screen in {"we_do", "you_do"}
            if st.button("Back", disabled=not back_enabled):
                if st.session_state.screen == "we_do":
                    st.session_state.screen = "i_do"
                elif st.session_state.screen == "you_do":
                    st.session_state.screen = "we_do"
                st.rerun()
        # Dev-only calibrate
        if st.query_params.get("dev") == "1":
            if st.button("Calibrate overlays"):
                st.session_state.screen = "calibrate"
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

        # Static visual: only the image background with no overlay labels
        check_html = """
        <div class="check-real" role="img" aria-label="Check background"></div>
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
    scenario_idx = 0  # I do uses first scenario
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
        if guided.get("context"):
            st.info(guided["context"])

        # Progress info
        progress_ratio = 0.0 if current_clamped < 0 else (current_clamped + 1) / total_steps
        st.progress(progress_ratio, text=f"Step {max(0, current_clamped + 1)} of {total_steps}")

        # Percent-based hotspot positions to align with typical personal check layout
        positions = _load_overlay_positions()
        # Ensure background image is applied inline to avoid CSS timing issues
        bg_url = _get_check_bg_data_url()

        # Use native HTML overlay in I do to avoid component load timing in some environments
        def style_box(key: str, active: bool) -> str:
            p = positions[key]
            hi = "outline:2px solid var(--color-bright-blue); outline-offset:2px;" if active else ""
            return f"left:{p['left']}%; top:{p['top']}%; width:{p['width']}%; height:{p['height']}%; {hi}"

        if bg_url:
            parts = [f"<div class='check-real' style=\"background-image:url('{bg_url}'); background-size:cover; background-position:center;\">"]
        else:
            parts = ["<div class='check-real'>"]
        parts.append(f"<div class='hotspot' style='{style_box('date', current_clamped==0)}'><div class='fill'>{fields['date']}</div></div>")
        parts.append(f"<div class='hotspot' style='{style_box('payee', current_clamped==1)}'><div class='fill'>{fields['payee']}</div></div>")
        # Remove leading $ if present, since the check already shows it
        amt = fields['amount_numeric'].lstrip('$').strip()
        parts.append(f"<div class='hotspot' style='{style_box('amount_numeric', current_clamped==2)}'><div class='fill' style='right:10px; left:auto;'>{amt}</div></div>")
        parts.append(f"<div class='hotspot' style='{style_box('amount_words', current_clamped==3)}'><div class='fill'>{fields['amount_words']}</div></div>")
        parts.append(f"<div class='hotspot' style='{style_box('memo', current_clamped==4)}'><div class='fill'>{fields['memo']}</div></div>")
        parts.append(f"<div class='hotspot' style='{style_box('signature', current_clamped==5)}'><div class='fill signature-text'>{fields['signature']}</div></div>")
        # Popover tip near the active field
        if current_clamped >= 0:
            active = steps[current_clamped]["field"]
            p = positions[active]
            # Force above for dollar amount and signature to avoid covering content
            force_above = active in {"amount_numeric", "signature"}
            place_above = force_above or (p['top'] > 12)
            if place_above:
                # Offset by the field's height plus extra margin
                tip_top = max(0, p['top'] - (p['height'] + 6))
                cls = 'tip above'
            else:
                tip_top = p['top'] + p['height'] + 2
                cls = 'tip below'
            # Prefer placing a bit to the right; clamp within bounds
            tip_left = min(95, max(0, p['left'] + 4))
            parts.append(
                f"<div class='{cls}' style='left:{tip_left}%; top:{tip_top}%;'>{steps[current_clamped]['explanation']}</div>"
            )
        parts.append("</div>")
        st.markdown("\n".join(parts), unsafe_allow_html=True)

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


def _normalize_amount_words(text: str) -> str:
    """Looser normalization for amount-in-words.
    - case-insensitive
    - ignore 'dollar(s)', 'and', 'only'
    - allow hyphens vs spaces
    - keep the cents fraction like 00/100
    """
    t = text.lower().strip()
    t = t.replace('-', ' ')
    # keep fraction intact, strip punctuation except / digits
    allowed = set("abcdefghijklmnopqrstuvwxyz 0123456789/ ")
    t = ''.join(ch if ch in allowed else ' ' for ch in t)
    tokens = [tok for tok in t.split() if tok not in {"dollar", "dollars", "and", "only"}]
    return " ".join(tokens)


def _validate_amount_words(value: str, expected: str) -> tuple[bool, str | None]:
    if _normalize_amount_words(value) == _normalize_amount_words(expected):
        return True, None
    return False, f"Example: {expected} (format flexible)"


def render_check_we_do() -> None:
    scenario_idx = 1  # We do uses second scenario (guided with prompts)
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
        we_context = guided.get("context", "Scenario (Nov 1, 2025): Jordan Patel pays Oakwood Apartments $1,200.00.")
        st.info(we_context)
        st.caption("We’ll fill one field at a time. Memo/signature are flexible. Click Next to proceed.")

        positions = _load_overlay_positions()
        bg_url = _get_check_bg_data_url()
        we_fields = ["date","payee","amount_numeric","amount_words","memo","signature"]
        # Allow clicking hotspots via query param to select field
        qp = st.query_params
        if qp.get("we_field") in we_fields:
            st.session_state.we_step = we_fields.index(qp.get("we_field"))
        idx = max(0, min(st.session_state.we_step, len(we_fields)-1))
        active_field = we_fields[idx]

        # Draw check overlays
        def style_box(key: str, active: bool) -> str:
            p = positions[key]
            hi = "outline:2px solid var(--color-bright-blue); outline-offset:2px;" if active else ""
            return f"left:{p['left']}%; top:{p['top']}%; width:{p['width']}%; height:{p['height']}%; {hi}"
        parts = [f"<div class='check-real' style=\"background-image:url('{bg_url or ''}'); background-size:cover; background-position:center;\">"]
        parts.append(f"<a href='?we_field=date' class='hotspot' style='{style_box('date', active_field=='date')}'><div class='fill'>{st.session_state.we_date}</div></a>")
        parts.append(f"<a href='?we_field=payee' class='hotspot' style='{style_box('payee', active_field=='payee')}'><div class='fill'>{st.session_state.we_payee}</div></a>")
        parts.append(f"<a href='?we_field=amount_numeric' class='hotspot' style='{style_box('amount_numeric', active_field=='amount_numeric')}'><div class='fill' style='right:10px; left:auto;'>{st.session_state.we_amount_numeric}</div></a>")
        parts.append(f"<a href='?we_field=amount_words' class='hotspot' style='{style_box('amount_words', active_field=='amount_words')}'><div class='fill'>{st.session_state.we_amount_words}</div></a>")
        parts.append(f"<a href='?we_field=memo' class='hotspot' style='{style_box('memo', active_field=='memo')}'><div class='fill'>{st.session_state.we_memo}</div></a>")
        parts.append(f"<a href='?we_field=signature' class='hotspot' style='{style_box('signature', active_field=='signature')}'><div class='fill signature-text'>{st.session_state.we_signature}</div></a>")
        # Tip near active field
        p = positions[active_field]
        tip_top = max(0, p['top'] - (p['height'] + 6))
        tip_left = min(95, max(0, p['left'] + 4))
        instruction_map = {
            "date": "Enter the date in MM/DD/YYYY (e.g., 11/01/2025).",
            "payee": "Type the payee exactly: Oakwood Apartments.",
            "amount_numeric": "Enter the numeric amount 1200.00",
            "amount_words": "Write the amount in words with the cents fraction.",
            "memo": "Add a memo (optional).",
            "signature": "Sign your name (flexible).",
        }
        parts.append(f"<div class='tip above' style='left:{tip_left}%; top:{tip_top}%;'>Step {idx+1} of {len(we_fields)} — {instruction_map[active_field]}</div>")
        parts.append("</div>")
        st.markdown("\n".join(parts), unsafe_allow_html=True)

        # Active input below (mirrors on-check value)
        ok, msg = False, None
        if active_field == "date":
            st.session_state.we_date = st.text_input("Date (MM/DD/YYYY)", value=st.session_state.we_date, placeholder="11/01/2025")
            ok, msg = _validate_date(st.session_state.we_date) if st.session_state.we_date else (False, None)
        elif active_field == "payee":
            st.session_state.we_payee = st.text_input("Pay to the Order of", value=st.session_state.we_payee, placeholder=expected["payee"])
            ok, msg = _validate_payee(st.session_state.we_payee, expected["payee"]) if st.session_state.we_payee else (False, None)
        elif active_field == "amount_numeric":
            st.session_state.we_amount_numeric = st.text_input("$ Amount (numeric)", value=st.session_state.we_amount_numeric, placeholder=expected["amount_numeric"]).lstrip('$').strip()
            ok, msg = _validate_amount_numeric(st.session_state.we_amount_numeric, expected["amount_numeric"]) if st.session_state.we_amount_numeric else (False, None)
        elif active_field == "amount_words":
            st.session_state.we_amount_words = st.text_input("Amount in Words", value=st.session_state.we_amount_words, placeholder=expected["amount_words"]) 
            ok, msg = _validate_amount_words(st.session_state.we_amount_words, expected["amount_words"]) if st.session_state.we_amount_words else (False, None)
        elif active_field == "memo":
            st.session_state.we_memo = st.text_input("Memo (optional)", value=st.session_state.we_memo)
            ok, msg = True, None
        else:
            st.session_state.we_signature = st.text_input("Signature", value=st.session_state.we_signature)
            ok = len(st.session_state.we_signature.strip()) > 0
            msg = None if ok else "Add your signature"

        if msg is not None:
            st.markdown(
                f"<div role='status' aria-live='polite' class='{'field-ok' if ok else 'field-error'}'>{'Looks good' if ok else msg}</div>",
                unsafe_allow_html=True,
            )

        nav_l, nav_r = st.columns([1,1])
        with nav_l:
            if st.button("Back step", disabled=idx == 0):
                st.session_state.we_step = max(0, idx-1)
                st.rerun()
        with nav_r:
            disable_next = (not ok) if active_field in {"payee","amount_numeric"} else False
            if st.button("Next step", disabled=idx == len(we_fields)-1 or disable_next):
                st.session_state.we_step = min(len(we_fields)-1, idx+1)
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


def render_check_you_do() -> None:
    scenario_idx = 2  # You do uses third scenario (independent)
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

        positions = _load_overlay_positions()
        bg = _get_check_bg_data_url()
        values = {
            "date": st.session_state.you_date,
            "payee": st.session_state.you_payee,
            "amount_numeric": st.session_state.you_amount_numeric,
            "amount_words": st.session_state.you_amount_words,
            "memo": st.session_state.you_memo,
            "signature": st.session_state.you_signature,
        }
        try:
            updated = _check_overlay_component(bg_url=bg, positions=positions, values=values, editable=True)
        except Exception:
            html = ["<div class='check-real'>"]
            def ip(name):
                p = positions[name]
                style = f"left:{p['left']}%; top:{p['top']}%; width:{p['width']}%; height:{p['height']}%;"
                val = values.get(name, "")
                return f"<textarea style='position:absolute; {style}; resize:none; border:2px dashed var(--color-bright-blue); border-radius:6px; background:rgba(255,255,255,0.02); padding:6px 10px;' name='{name}'>{val}</textarea>"
            for k in ["date","payee","amount_numeric","amount_words","memo","signature"]:
                html.append(ip(k))
            html.append("</div>")
            st.markdown("\n".join(html), unsafe_allow_html=True)
            updated = values
        st.session_state.you_date = updated.get("date", "")
        st.session_state.you_payee = updated.get("payee", "")
        st.session_state.you_amount_numeric = updated.get("amount_numeric", "").lstrip('$').strip()
        st.session_state.you_amount_words = updated.get("amount_words", "")
        st.session_state.you_memo = updated.get("memo", "")
        st.session_state.you_signature = updated.get("signature", "")

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
    if screen == "i_do":
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
    elif screen == "calibrate":
        render_calibrate()


def render_calibrate() -> None:
    positions = _load_overlay_positions() or st.session_state["overlay_positions"]
    with st.container():
        st.markdown('<div class="ngpf-container">', unsafe_allow_html=True)
        st.markdown("### Calibrate overlays (dev-only)")
        st.caption("Adjust sliders to align boxes with your check image. Save when satisfied.")

        # Controls first so updated values are used immediately when rendering preview below
        col_left, col_right = st.columns(2)

        def sliders_for(name: str, column):
            with column:
                st.markdown(f"**{name.replace('_',' ').title()}**")
                p = positions[name]
                p["top"] = round(st.slider(f"{name}-top %", 0.0, 100.0, float(p["top"]), 0.5, key=f"{name}_top"), 1)
                p["left"] = round(st.slider(f"{name}-left %", 0.0, 100.0, float(p["left"]), 0.5, key=f"{name}_left"), 1)
                p["width"] = round(st.slider(f"{name}-width %", 1.0, 100.0, float(p["width"]), 0.5, key=f"{name}_width"), 1)
                p["height"] = round(st.slider(f"{name}-height %", 1.0, 100.0, float(p["height"]), 0.5, key=f"{name}_height"), 1)

        sliders_for("date", col_left)
        sliders_for("payee", col_left)
        sliders_for("amount_numeric", col_left)
        sliders_for("amount_words", col_right)
        sliders_for("memo", col_right)
        sliders_for("signature", col_right)

        st.divider()

        # Live preview uses latest slider values
        html = ["<div class='check-real'>"]
        for key, label in [
            ("date", "DATE"),
            ("payee", "PAYEE"),
            ("amount_numeric", "$ NUMERIC"),
            ("amount_words", "AMOUNT WORDS"),
            ("memo", "MEMO"),
            ("signature", "SIGNATURE"),
        ]:
            p = positions[key]
            style = f"left:{p['left']}%; top:{p['top']}%; width:{p['width']}%; height:{p['height']}%;"
            html.append(f"<div class='cal-box' style='{style}'>{label}</div>")
        html.append("</div>")
        st.markdown("\n".join(html), unsafe_allow_html=True)

        save_col, cancel_col = st.columns(2)
        with save_col:
            if st.button("Save positions", type="primary"):
                _save_overlay_positions(positions)
                st.success("Saved to assets/overlay.json")
        with cancel_col:
            if st.button("Back to I do"):
                st.session_state.screen = "i_do"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()


