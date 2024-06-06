import streamlit as st
from utils.data.load_data import load_vocab, load_pickle_file
from utils.prediction.text_completion import predict_next_word
from utils.text_processing.edit_distance import edits1, edits2, edits3
from utils.text_processing.text_preprocessing import text_processing


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
        # Sidebar title
        st.sidebar.title("Text Editing and Completion")

        # Feature selection
        feature = st.sidebar.selectbox(
            "Choose a feature",
            (
                "Interactive Autocomplete",
                "Autocorrect",
                "Combined Autocomplete and Autocorrect",
            ),
        )

        # Configuration parameters
        if feature in (
            "Interactive Autocomplete",
            "Combined Autocomplete and Autocorrect",
        ):
            num_words = st.sidebar.slider("Number of words to complete", 1, 10, 5)
            model_type = st.sidebar.selectbox("Model type", ("N-gram", "LSTM"))

        # Additional parameters
        if feature == "Combined Autocomplete and Autocorrect":
            autocorrect_level = st.sidebar.slider("Autocorrect level", 1, 5, 3)

        col1, col2 = st.columns(2)
        # Prediction
        prediction = "suggestion"

        # Load the vocabulary, n-gram counts, and n-gram+1 counts from files
        vocab = load_vocab("src/models/vocabulary.txt")
        ngram_counts = load_pickle_file("src/models/ngram_counts.pkl")
        nplus1gram_counts = load_pickle_file("src/models/nplus1gram_counts.pkl")

        # Define session state variables for the selected feature
        if f"{feature}_user_input" not in st.session_state:
            st.session_state[f"{feature}_user_input"] = ""
        if f"{feature}_predicted_text" not in st.session_state:
            st.session_state[f"{feature}_predicted_text"] = ""

        with col1:
            # Text input
            user_input = st.text_area(
                "Start typing:",
                value=st.session_state[f"{feature}_user_input"],
            )

            if st.button("Predict"):
                # Process the user's input
                prev_tokens = text_processing(str(user_input))
                # Predict the next word
                next_word_prediction, prob, _ = predict_next_word(
                    prev_tokens, ngram_counts, nplus1gram_counts, vocab
                )
                # Update 'predicted_text' in the session state
                st.session_state[f"{feature}_predicted_text"] = (
                    str(user_input) + " " + next_word_prediction
                )

        with col2:
            suggested_text = st.text_area(
                "Predicted text:",
                value=st.session_state[f"{feature}_predicted_text"],
                disabled=True,
                key="suggested_text_1",
            )

            if st.button("Apply suggestion", key="suggested_b_1"):
                # Update 'user_input' in the session state
                st.session_state[f"{feature}_user_input"] = st.session_state[
                    f"{feature}_predicted_text"
                ]
                st.rerun()  # Rerun the script to update the text area


show()
