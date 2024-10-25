import streamlit as st

# Page title
st.set_page_config(page_title="Text Flow!", layout="centered")
st.markdown(
    """
    <style>
    a[href$="/"] {display: none;}

        a[href*="/home"]{
            display: none;
        }
        a[href*="/autocomplet"]{
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def show():
    # Page title
    st.markdown(
        "<h1 style='text-align: center; color: black;'>Text Flow</h1>",
        unsafe_allow_html=True,
    )

    st.image("static/images/text_typing_image (1).png")
    if st.button("Start", use_container_width=True):
        st.switch_page("pages/home.py")


show()
