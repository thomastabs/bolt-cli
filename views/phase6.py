import streamlit as st

st.title("Phase 6 · Maintenance")
st.caption("Fix-Bolt & Vaccine Records — context-isolated bug diagnosis with permanent fix history")
st.divider()
st.info(
    "Coming in the next iteration.  \n"
    "Fetches a Taiga issue, accepts only the bug description + stack trace + isolated code snippet "
    "(the full `.ai-context.md` is never passed — Context Isolation Rule), proposes a minimal patch, "
    "and on approval appends a permanent Vaccine Record to context."
)
