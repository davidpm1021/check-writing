"""NGPF Check Writing Interactive — Sprint 1 UI

Scaffold with global styles, header, responsive container, controls, and static Check UI.
No external calls, no persistence beyond session.
"""

from __future__ import annotations

import streamlit as st

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


def inject_global_styles() -> None:
    """Inject CSS variables, fonts, focus styles, and basic layout tokens."""
    css = f"""
    <style>
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
      }}
      h1 {{
        font-family: {design_tokens.HEADLINE_FONT};
        font-weight: 700;
        font-size: 48px;
        line-height: 1.2;
        color: var(--color-royal-blue);
        margin: 0;
      }}

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

      /* Check visual */
      .check {{
        width: 100%;
        background: #fff;
        border: 2px solid var(--color-light-gray-blue);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
      }}
      .check-row {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-bottom: 12px;
      }}
      .check-label {{
        font-weight: 600;
        color: var(--color-navy-blue);
        margin-bottom: 4px;
      }}
      .check-box {{
        height: 40px;
        border: 1px solid var(--color-light-gray-blue);
        border-radius: 8px;
        background: var(--color-soft-blue-tint);
        position: relative;
      }}
      .check-box.wide {{ height: 56px; }}
      .check-fill {{
        position: absolute;
        inset: 0;
        display: flex;
        align-items: center;
        padding: 0 10px;
        color: var(--color-navy-blue);
        font-weight: 600;
      }}
      .check-amount {{
        display: grid;
        grid-template-columns: 1fr 180px;
        gap: 12px;
      }}
      @media (max-width: 480px) {{
        .check-row, .check-amount {{ grid-template-columns: 1fr; }}
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
    ]


def render_controls() -> None:
    with st.container():
        st.markdown('<div class="ngpf-container">', unsafe_allow_html=True)
        st.markdown('<div class="ngpf-controls" role="region" aria-label="Controls">', unsafe_allow_html=True)
        scenarios = _get_scenarios()
        scenario_titles = [s["title"] for s in scenarios]
        st.session_state.selected_scenario = st.selectbox(
            "Scenario",
            options=list(range(len(scenario_titles))),
            format_func=lambda i: scenario_titles[i],
            index=st.session_state.selected_scenario,
            help="Pick a built-in example to practice.",
        )

        tabs = st.tabs(["I do", "We do", "You do"])
        with tabs[0]:
            st.session_state.mode = "I do"
            st.caption("Guided walkthrough — auto-fills with explanations.")
        with tabs[1]:
            st.session_state.mode = "We do"
            st.caption("Semi-guided — prompts, hints, and inline corrections.")
        with tabs[2]:
            st.session_state.mode = "You do"
            st.caption("Independent practice — minimal prompts with inline correction.")

        if st.button("Reset", type="secondary", help="Clear and start over"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Detect scenario or mode changes to reset guided state
    if (
        st.session_state.selected_scenario != st.session_state._last_scenario
        or st.session_state.mode != st.session_state._last_mode
    ):
        st.session_state.guided_step = -1
        st.session_state._last_scenario = st.session_state.selected_scenario
        st.session_state._last_mode = st.session_state.mode


def render_check_static() -> None:
    scenario = _get_scenarios()[st.session_state.selected_scenario]
    with st.container():
        st.markdown('<div class="ngpf-container">', unsafe_allow_html=True)
        st.markdown("#### Scenario", help="Use this prompt to fill out the check in later sprints.")
        st.info(scenario["prompt"])

        # Static visual of a check
        check_html = """
        <div class="check" role="group" aria-label="Check fields (static)">
          <div class="check-row">
            <div>
              <div class="check-label">Date</div>
              <div class="check-box"></div>
            </div>
            <div>
              <div class="check-label">Pay to the Order of</div>
              <div class="check-box"></div>
            </div>
          </div>

          <div class="check-amount">
            <div>
              <div class="check-label">Amount in Words</div>
              <div class="check-box wide"></div>
            </div>
            <div>
              <div class="check-label">$ Amount</div>
              <div class="check-box"></div>
            </div>
          </div>

          <div class="check-row">
            <div>
              <div class="check-label">Memo</div>
              <div class="check-box"></div>
            </div>
            <div>
              <div class="check-label">Signature</div>
              <div class="check-box"></div>
            </div>
          </div>
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

        # Check with filled fields
        check_html = f"""
        <div class=\"check\" role=\"group\" aria-label=\"Check fields (guided)\"> 
          <div class=\"check-row\"> 
            <div>
              <div class=\"check-label\">Date</div>
              <div class=\"check-box\"><div class=\"check-fill\">{fields['date']}</div></div>
            </div>
            <div>
              <div class=\"check-label\">Pay to the Order of</div>
              <div class=\"check-box\"><div class=\"check-fill\">{fields['payee']}</div></div>
            </div>
          </div>
          <div class=\"check-amount\">
            <div>
              <div class=\"check-label\">Amount in Words</div>
              <div class=\"check-box wide\"><div class=\"check-fill\">{fields['amount_words']}</div></div>
            </div>
            <div>
              <div class=\"check-label\">$ Amount</div>
              <div class=\"check-box\"><div class=\"check-fill\">{fields['amount_numeric']}</div></div>
            </div>
          </div>
          <div class=\"check-row\">
            <div>
              <div class=\"check-label\">Memo</div>
              <div class=\"check-box\"><div class=\"check-fill\">{fields['memo']}</div></div>
            </div>
            <div>
              <div class=\"check-label\">Signature</div>
              <div class=\"check-box\"><div class=\"check-fill\">{fields['signature']}</div></div>
            </div>
          </div>
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


def main() -> None:
    inject_global_styles()
    _ensure_session_state_defaults()
    render_header()
    # Layout: controls left, check right
    left, right = st.columns([1, 2], gap="large")
    with left:
        render_controls()
    with right:
        if st.session_state.mode == "I do":
            render_check_guided()
        else:
            render_check_static()


if __name__ == "__main__":
    main()


