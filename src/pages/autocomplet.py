import streamlit as st
from utils.data.load_data import load_vocab, load_pickle_file
from utils.prediction.text_completion import predict_next_word, predict_next_n_words
from utils.text_processing.edit_distance import edits1, edits2, edits3
from utils.text_processing.text_preprocessing import text_processing
from utils.prediction.text_correction import correct_text


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

        # Check if the feature is either 'Autocorrect' or 'Combined Autocomplete and Autocorrect'
        if feature in ("Autocorrect", "Combined Autocomplete and Autocorrect"):
            # Load the unigram, bigram, and trigram counters from pickle files
            unigram_counter = load_pickle_file("src/models/unigram_counter.pkl")
            bigram_counter = load_pickle_file("src/models/bigram_counter.pkl")
            trigram_counter = load_pickle_file("src/models/trigram_counter.pkl")

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
                # If the feature is 'Autocorrect' or 'Combined Autocomplete and Autocorrect'
                if feature in ("Autocorrect", "Combined Autocomplete and Autocorrect"):
                    # Correct the user's input text
                    corrected_text = correct_text(
                        str(user_input),
                        vocab,
                        edits1,
                        edits2,
                        unigram_counter,
                        bigram_counter,
                        trigram_counter,
                    )
                    # Store the corrected text in the session state
                    st.session_state[f"{feature}_predicted_text"] = corrected_text
                    if feature == "Combined Autocomplete and Autocorrect":
                        user_input = corrected_text

                # Process the user's input
                prev_tokens = text_processing(str(user_input))
                if feature in (
                    "Interactive Autocomplete",
                    "Combined Autocomplete and Autocorrect",
                ):
                    # If only one word is to be predicted
                    if num_words == 1:

                        # Predict the next word
                        next_word_prediction, prob, _ = predict_next_word(
                            prev_tokens, ngram_counts, nplus1gram_counts, vocab
                        )
                    else:
                        # Predict the next 'num_words' words
                        next_word_prediction = predict_next_n_words(
                            prev_tokens,
                            ngram_counts,
                            nplus1gram_counts,
                            vocab,
                            num_words,
                        )
                    # Update 'predicted_text' in the session state
                    st.session_state[f"{feature}_predicted_text"] = (
                        str(user_input) + " " + next_word_prediction
                    )

        with col2:
            # Display the predicted text in a text area
            suggested_text = st.text_area(
                "Predicted text:",
                value=st.session_state[f"{feature}_predicted_text"],
                disabled=True,
                key="suggested_text_1",
            )

            # Check if the 'Apply suggestion' button is clicked
            if st.button("Apply suggestion", key="suggested_b_1"):
                # Update 'user_input' in the session state
                st.session_state[f"{feature}_user_input"] = st.session_state[
                    f"{feature}_predicted_text"
                ]
                st.rerun()  # Rerun the script to update the text area


show()
