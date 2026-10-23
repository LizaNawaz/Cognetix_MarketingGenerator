"""
Main application entry point for the Cognetix GenAI project.
"""

import streamlit as st


def main():
    """Render the starter Streamlit application."""
    st.set_page_config(
        page_title="Cognetix GenAI Project",
        page_icon="🤖",
        layout="wide",
    )

    st.title("Cognetix GenAI Project")
    st.write("Welcome! Replace this placeholder with your application.")

    st.info(
        "Next steps: configure your LLM client, add prompts in src/, "
        "and create evaluations in eval/."
    )


if __name__ == "__main__":
    main()
