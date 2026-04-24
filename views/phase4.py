import streamlit as st

st.title("Phase 4 · QA Verification")
st.caption("QA & BDD Test Generation — generate test suites strictly from locked Gherkin")
st.divider()
st.info(
    "Coming in the next iteration.  \n"
    "Generates Cypress or Pytest-BDD test scripts exclusively from the approved Gherkin scenarios, "
    "saves them to `openspec/`, and moves the story to Staging in Taiga."
)
