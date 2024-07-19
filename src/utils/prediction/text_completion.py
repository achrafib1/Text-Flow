import numpy as np
import streamlit as st
from typing import Dict, Tuple, List, Optional
import tensorflow as tf
import keras


def calculate_probability(
    word: str,
    last_ngram: Tuple[str, ...],
    ngram_counts: Dict[Tuple[str, ...], int],
    nplus1gram_counts: Dict[Tuple[str, ...], int],
    vocab_size: int,
) -> float:
    """
    Calculates the probability of a word given the last n-gram using Laplace smoothing.

    Parameters:
    word (str): The word for which the probability is calculated.
    last_ngram (Tuple[str, ...]): The last n-gram before the word.
    ngram_counts (Dict[Tuple[str, ...], int]): The counts of each n-gram in the corpus.
    nplus1gram_counts (Dict[Tuple[str, ...], int]): The counts of each (n+1)-gram in the corpus.
    vocab_size (int): The number of unique words in the vocabulary.

    Returns:
    float: The calculated probability of the word.
    """
    # Get the count of the last n-gram
    ngram_count = ngram_counts.get(last_ngram, 0)

    # Get the count of the (n+1)-gram which is the last n-gram followed by the word
    nplus1gram_count = nplus1gram_counts.get(last_ngram + (word,), 0)

    # Calculate the probability with Laplace smoothing
    probability = np.log((nplus1gram_count + 1) / (ngram_count + vocab_size))

    return probability


@st.cache_data
def predict_next_word(
    previous_tokens: List[str],
    ngram_counts: Dict[Tuple[str, ...], int],
    nplus1gram_counts: Dict[Tuple[str, ...], int],
    vocab: List[str],
    start_of_word: Optional[str] = None,
) -> Tuple[str, float, Dict[str, float]]:
    """
    Predicts the next word based on the previous tokens using n-gram counts.

    Parameters:
    previous_tokens (List[str]): The list of previous tokens.
    ngram_counts (Dict[Tuple[str, ...], int]): The counts of each n-gram in the corpus.
    nplus1gram_counts (Dict[Tuple[str, ...], int]): The counts of each (n+1)-gram in the corpus.
    vocab (List[str]): The list of words in the vocabulary.
    start_of_word (Optional[str]): The starting characters of the word. Default is None.

    Returns:
    Tuple[str, float, Dict[str, float]]: The predicted next word, its probability, and the probabilities of all words.
    """
    # Determine the order of the n-grams
    n = len(list(ngram_counts.keys())[0])

    # Get the last n tokens
    last_ngram = tuple(previous_tokens[-n:])

    # Filter the vocabulary to only include words that start with the given characters
    if start_of_word is not None:
        vocab = [word for word in vocab if word.startswith(start_of_word)]

    # Calculate the probabilities for each word in the vocabulary
    probabilities = {
        word: calculate_probability(
            word, last_ngram, ngram_counts, nplus1gram_counts, len(vocab)
        )
        for word in vocab
    }

    # Find the word with the highest probability
    next_word = max(probabilities, key=lambda x: probabilities.get(x, 0.0))
    max_probability = probabilities[next_word]

    return next_word, max_probability, probabilities


@st.cache_data
def predict_next_n_words(
    previous_tokens: List[str],
    ngram_counts: Dict[Tuple[str, ...], int],
    nplus1gram_counts: Dict[Tuple[str, ...], int],
    vocab: List[str],
    n_words: int,
    start_of_word: Optional[str] = None,
) -> str:
    """
    Predicts the next 'n_words' based on the previous tokens using n-gram counts.

    Parameters:
    previous_tokens (List[str]): The list of previous tokens.
    ngram_counts (Dict[Tuple[str, ...], int]): The counts of each n-gram in the corpus.
    nplus1gram_counts (Dict[Tuple[str, ...], int]): The counts of each (n+1)-gram in the corpus.
    vocab (List[str]): The list of words in the vocabulary.
    n_words (int): The number of words to predict.
    start_of_word (Optional[str]): The starting characters of the word. Default is None.

    Returns:
    str: The predicted next 'n_words' as a string.
    """
    # Placeholder for the predicted words
    words = []

    # Predict the next 'n_words'
    for _ in range(n_words):
        next_word, _, _ = predict_next_word(
            previous_tokens, ngram_counts, nplus1gram_counts, vocab, start_of_word
        )
        words.append(next_word)
        previous_tokens.append(next_word)

    # Return the predicted words as a string
    return " ".join(words)


@st.cache_data
def predict_next_word_lstm(
    initial_sentence: str,
    lstm_model,
    tokenizer,
    sequence_length: int = 1,
) -> str:
    """
    Predicts the next word based on the initial sentence using LSTM model.

    Parameters:
    initial_sentence (str): The initial sentence.
    lstm_model: The trained LSTM model.
    tokenizer: The trained tokenizer.
    sequence_length (int): The maximum length of the sequence. Default is 1.

    Returns:
    str: The predicted next word as a string.
    """
    # Tokenize the seed text
    tokenized_text = tokenizer.texts_to_sequences([initial_sentence])[0]

    # Pad the sequences
    padded_sequence = keras.preprocessing.sequence.pad_sequences(
        [tokenized_text], maxlen=sequence_length - 1, padding="pre"
    )

    # Get the probabilities of predicting a word
    prediction_probabilities = lstm_model.predict(padded_sequence, verbose=0)

    # Choose the next word based on the maximum probability
    predicted_index = np.argmax(prediction_probabilities, axis=-1).item()

    # Get the actual word from the word index
    predicted_word = tokenizer.index_word[predicted_index]

    # Return the predicted word
    return predicted_word


@st.cache_data
def predict_next_words_lstm(
    initial_sentence: str,
    lstm_model,
    tokenizer,
    max_len: int = 1,
) -> str:
    """
    Predicts the next 'max_len' words based on the initial sentence using LSTM model.

    Parameters:
    initial_sentence (str): The initial sentence.
    lstm_model: The trained LSTM model.
    tokenizer: The trained tokenizer.
    max_len (int): The maximum number of words to predict. Default is 1.

    Returns:
    str: The predicted next 'max_len' words as a string.
    """
    # Placeholder for the predicted words
    words = []

    # Predict the next 'max_len' words
    for _ in range(max_len):
        # Predict the next word
        next_word = predict_next_word_lstm(
            initial_sentence, lstm_model, tokenizer, max_len
        )

        # Append the predicted word to the list of words
        words.append(next_word)

        # Update the initial sentence for the next prediction
        initial_sentence += " " + next_word

    # Return the predicted words as a string
    return " ".join(words)
