"""
app.py — bolt entry point and central router

Runs on every page navigation. Responsibilities:
  - Page config (must be first)
  - CSS injection (before page content, prevents flash)
  - Navigation routing via st.navigation()
  - Shared sidebar

Adding a phase:
  1. Implement components/phase<N>.py  →  render_phase<N>()
  2. Create views/phase<N>.py          →  calls render_phase<N>()
  3. Add st.Page entry to _pages below
  4. Add label to components/sidebar._PHASES
"""

from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from components.sidebar import render_sidebar

load_dotenv()

st.set_page_config(
    page_title="bolt",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"<style>{Path('assets/style.css').read_text(encoding='utf-8')}</style>",
    unsafe_allow_html=True,
)

_pages = [
    st.Page("views/phase1.py", title="Phase 1 · Requirements", default=True),
    st.Page("views/phase2.py", title="Phase 2 · Design"),
    st.Page("views/phase3.py", title="Phase 3 · Implementation"),
    st.Page("views/phase4.py", title="Phase 4 · Testing"),
    st.Page("views/phase5.py", title="Phase 5 · Deployment"),
    st.Page("views/phase6.py", title="Phase 6 · Maintenance"),
]

pg = st.navigation(_pages, position="hidden")
render_sidebar()
pg.run()
