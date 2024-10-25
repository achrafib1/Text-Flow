import streamlit as st
import time


def show():
    # Page title
    st.set_page_config(page_title="Text Flow !", layout="centered")

    # Hide the app page
    st.markdown(
        """
    <style>
    a[href$="/"] {display: none;}

    </style>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Text Page"])

    if page == "Home":
        with st.container():
            st.title("Welcome to Text Flow !")

        # Introduction
        with st.container():
            st.header("Introduction", divider="orange")
            page_bg_img = "static/images/text_typing_image (2).png"
            st.write(
                """
        # Welcome to TextFlow, the future of seamless writing! 🚀
        TextFlow is an innovative application that revolutionizes the way you write. 
        Powered by advanced n-gram technology, it offers dynamic autocompletion and autocorrection features, making your writing experience smoother and more efficient.
        With TextFlow, you can say goodbye to typos and hello to flawless text. Our intelligent autocorrection feature catches and corrects errors as you type, ensuring your writing is always at its best. The autocompletion feature predicts and suggests the next words, helping you write faster and with more confidence.
        Designed with a user-friendly interface using Streamlit, TextFlow is not just an application, it’s your personal writing assistant. It’s perfect for everyone, whether you’re a student working on an assignment, a professional drafting an email, or a writer crafting your next masterpiece.
        Experience the joy of effortless writing with TextFlow. Start your journey today and let your words flow! 📝
        """
            )
        st.image(page_bg_img)
        # Navigation
        with st.container():
            st.header("start writing your text")
            if st.button("Start", use_container_width=True):
                st.markdown(
                    f"""<style>
                                [data-testid="stAppViewContainer"] > .main {{
                                background-color: rgba(0,0,0,0.2);
                                }}
                        </style>
                                """,
                    unsafe_allow_html=True,
                )
                with st.spinner("Let's start our text writing journey!"):
                    # Simulate a delay
                    time.sleep(2)
                st.markdown(
                    f"""<style>
                                [data-testid="stAppViewContainer"] > .main {{
                                background-color: rgba(0,0,0,0);
                                }}
                        </style>
                                """,
                    unsafe_allow_html=True,
                )
                st.switch_page("pages/autocomplet.py")
    if page == "Text Page":
        st.switch_page("pages/autocomplet.py")

    # Footer
    with st.container():
        st.subheader("", divider="orange")
        st.write(
            """
        Made with ❤️ by name
        """
        )


show()
