import streamlit as st

st.title("Phase 2 · Architecture")
st.caption("Design & Architecture — generate OpenAPI specs and DB schemas anchored to approved Gherkin")
st.divider()
st.info(
    "Coming in the next iteration.  \n"
    "Reads the locked Gherkin from `openspec/.ai-context.md`, generates a formal "
    "OpenAPI 3.0 contract via AI, and appends the Technical Spec to context after human approval."
)
