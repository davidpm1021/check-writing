"""NGPF Check Writing Interactive — Sprint 0 scaffold

Streamlit skeleton with global styles, header, and responsive container.
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


def render_home() -> None:
    with st.container():
        st.markdown('<div class="ngpf-container">', unsafe_allow_html=True)
        st.success(
            "Sprint 0 scaffold loaded. Next: build Check UI and mode controls in Sprint 1."
        )
        st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    inject_global_styles()
    render_header()
    render_home()


if __name__ == "__main__":
    main()


