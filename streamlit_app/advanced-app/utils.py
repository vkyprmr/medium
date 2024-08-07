# Imports
import re

import streamlit as st

# Custom CSS
def load_css(file_path: str) -> None:
    """
    Load custom CSS file.

    Parameters
    ----------
    file_path : str
        Path to the CSS file.
    
    Returns
    -------
    None
    """
    with open(file_path, "r", encoding="utf-8") as f:
        custom_css = f.read()

    # Removing the lines that start after the lines /* Stylable containers */
    streamlit_css = custom_css.split("/* Stylable containers */")[0]
    st.markdown(f"<style>{streamlit_css}</style>", unsafe_allow_html=True)

    # Regular expression to find selectors starting with .stylable- and their rules
    pattern = re.compile(r'(\.stylable-[^{\s]+)\s*\{([^}]+)\}')
    # Find all matches
    matches = pattern.findall(custom_css)

    # Creating a dictionary
    stylable_css_dict = {
        selector.replace(".", ""): f"{ {rules.strip()} }" for selector, rules in matches
    }
    stylable_css_dict = {
        k: v.replace("'", "").replace("\\n", "") for k, v in stylable_css_dict.items()
    }
    st.session_state["stylable_css"] = stylable_css_dict
