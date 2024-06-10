import numpy as np
import streamlit as st


def calculate_probability(
    word, last_ngram, ngram_counts, nplus1gram_counts, vocab_size
):
    # Calculate the probability of the word given the last n-gram
    ngram_count = ngram_counts.get(last_ngram, 0)
    nplus1gram_count = nplus1gram_counts.get(last_ngram + (word,), 0)
    probability = np.log((nplus1gram_count + 1) / (ngram_count + vocab_size))

    return probability


@st.cache_data
def predict_next_word(
    previous_tokens, ngram_counts, nplus1gram_counts, vocab, start_of_word=None
):

    n = len(list(ngram_counts.keys())[0])

    # Get the last n tokens
    last_ngram = tuple(previous_tokens[-n:])
    print(last_ngram)

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
    next_word = max(probabilities, key=probabilities.get)
    max_probability = probabilities[next_word]

    return next_word, max_probability, probabilities


def predict_next_n_words(
    previous_tokens, ngram_counts, nplus1gram_counts, vocab, n_words, start_of_word=None
):
    words = []
    for _ in range(n_words):
        next_word, _, _ = predict_next_word(
            previous_tokens, ngram_counts, nplus1gram_counts, vocab, start_of_word
        )
        words.append(next_word)
        previous_tokens.append(next_word)
    return words
