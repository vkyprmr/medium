# Imports
import pandas as pd
import streamlit as st
from streamlit_extras.stylable_container import stylable_container


# Setting a page config
st.set_page_config(
    page_title="Basic Streamlit App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar
st.sidebar.title("Basic Streamlit App")
st.sidebar.write("This is a basic Streamlit app.")

# Main
st.title("Basic Streamlit App")
st.write("This is a basic Streamlit app.")

# Button
if st.button("Click me to show a dataframe!",
             use_container_width=True):
    st.write("You clicked the button!")

    # Dataframe
    df = pd.DataFrame({
        "A": [1, 2, 3, 4],
        "B": [10, 20, 30, 40],
    })
    st.dataframe(df)

# Stylable button
with stylable_container(
    key="green_button",
    css_styles=[
        """
        button {
            background-color: green;
            border-radius: 25px;
            color: white;
            border: none;
        }
        """,
        """
        button:hover {
            background-color: darkgreen;
        }
        """
    ]
):
    if st.button("Click me to release the ballons!",
                 use_container_width=True,
                 key="green_button"):
        st.balloons()


# Stylable markdown
with stylable_container(
    key="red_markdown",
    css_styles=[
        """
        p {
            color: red;
            font-size: 24px;
        }
        """
    ]
):
    st.markdown("This is a red markdown text.")

# You can even write markdown directly with custom css
st.write("You can even write markdown directly with custom css.")
st.code(
    """
    st.markdown(
        \"\"\"
        <p style="color: blue; font-size: 24px;">This is a blue markdown text.</p>
        \"\"\",
        unsafe_allow_html=True
    )
    """
)
st.markdown(
    """
    <p style="color: blue; font-size: 24px;">This is a blue markdown text.</p>
    """,
    unsafe_allow_html=True
)

# Expander
with st.expander("Expand me!"):
    st.write("This is an expander.")

# Popover
with st.popover("Pop me!"):
    st.write("This is a popover.")

if st.sidebar.button("Reset",
                     use_container_width=True):
    st.write("Resetting the app...")
    st.rerun()
