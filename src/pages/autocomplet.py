import streamlit as st


def show():
    st.set_page_config(page_title="Text Page", layout="wide")
    st.markdown(
        "<style>  ul[data-testid=stSidebarNavItems]  {display: none;} </style>",
        unsafe_allow_html=True,
    )
    st.sidebar.title("Navigation")
    images = []
    page = st.sidebar.radio("Go to", ["Text Page", "Home"])
    st.sidebar.markdown(
        '<hr style="border: 0.9px solid orange">', unsafe_allow_html=True
    )
    if page == "Home":
        st.title("Home Page")
        st.switch_page("pages/home.py")
    if page == "Text Page":
        st.title("Text Page")
        col1, col2 = st.columns(2)

        with col1:
            user_input = st.text_area("Start typing:")

        with col2:
            st.text_area("Predicted text:", value=user_input)


show()
