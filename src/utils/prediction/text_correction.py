import numpy as np
from utils.text_processing.text_preprocessing import text_processing
from typing import Dict, Optional, Tuple


def calculate_probability(
    word: str,
    unigram_counts: Dict[str, int],
    prev_word: Optional[str] = None,
    next_word: Optional[str] = None,
    bigram_counts: Optional[Dict[Tuple[str, str], int]] = None,
    trigram_counts: Optional[Dict[Tuple[str, str, str], int]] = None,
) -> float:
    """
    Calculates the combined probability of a word given its context (previous and next words).
    It uses unigram, bigram, and trigram counts to calculate probabilities with smoothing.
    The function returns the highest order n-gram probability available.

    Parameters:
    word (str): The word for which the probability is calculated.
    unigram_counts (Dict[str, int]): The counts of each unigram in the corpus.
    prev_word (Optional[str]): The word preceding the target word. Default is None.
    next_word (Optional[str]): The word following the target word. Default is None.
    bigram_counts (Optional[Dict[Tuple[str, str], int]]): The counts of each bigram in the corpus. Default is None.
    trigram_counts (Optional[Dict[Tuple[str, str, str], int]]): The counts of each trigram in the corpus. Default is None.

    Returns:
    float: The combined probability of the word.
    """
    # Calculate the individual word probability with smoothing
    word_prob = np.log(
        (unigram_counts.get(word, 0) + 1)
        / (sum(unigram_counts.values()) + len(unigram_counts))
    )

    combined_prob = word_prob

    if prev_word and bigram_counts is not None:
        # Calculate the conditional probability of the word given the previous word with smoothing
        bigram = (prev_word, word)
        bigram_prob = np.log(
            (bigram_counts.get(bigram, 0) + 1)
            / (unigram_counts.get(prev_word, 0) + len(unigram_counts))
        )
        combined_prob = bigram_prob

    if next_word and bigram_counts is not None:
        # Calculate the conditional probability of the word given the next word with smoothing
        bigram = (word, next_word)
        bigram_prob = np.log(
            (bigram_counts.get(bigram, 0) + 1)
            / (unigram_counts.get(next_word, 0) + len(unigram_counts))
        )
        combined_prob = bigram_prob

    if prev_word and next_word and trigram_counts and bigram_counts is not None:
        # Calculate the conditional probability of the word given the previous and next words with smoothing
        trigram = (prev_word, word, next_word)
        trigram_prob = np.log(
            (trigram_counts.get(trigram, 0) + 1)
            / (bigram_counts.get((prev_word, next_word), 0) + len(bigram_counts))
        )
        combined_prob = trigram_prob

    return combined_prob


def filter_known_words(words, vocab):
    "The subset of `words` that appear in the `vocab`."
    return set(words).intersection(vocab)


def correct(
    word,
    prev_word,
    next_word,
    vocab,
    edit1,
    edit2,
    unigram_counts,
    bigram_counts,
    trigram_counts,
):
    "Find the best correct spelling for `word`."

    # Generate candidate words

    candidates = (
        filter_known_words([word], vocab)
        | filter_known_words(edit1(word), vocab)
        | filter_known_words(edit2(word), vocab)
    )

    # Calculate the probability for each candidate word
    probs = {
        candidate: calculate_probability(
            candidate,
            unigram_counts,
            prev_word,
            next_word,
            bigram_counts,
            trigram_counts,
        )
        for candidate in candidates
    }

    # Return the candidate word with the highest probability
    return max(probs, key=probs.get), max(probs.values())


def correct_text(
    text, vocab, edit1, edit2, unigram_counts, bigram_counts, trigram_counts
):
    # Tokenize and process the text
    words = text_processing(text)

    # Initialize an empty list to hold the corrected words
    corrected_words = []

    # Iterate over each word in the text
    for i, word in enumerate(words):
        # If the word is not in the vocabulary, it's considered a misspelled word
        if word not in vocab:
            # Get the previous and next words
            prev_word = words[i - 1] if i > 0 else ""
            next_word = words[i + 1] if i < len(words) - 1 else ""

            # Correct the misspelled word
            corrected_word, _ = correct(
                word,
                prev_word,
                next_word,
                vocab,
                edit1,
                edit2,
                unigram_counts,
                bigram_counts,
                trigram_counts,
            )

            # Add the corrected word to the list
            corrected_words.append(corrected_word)
        else:
            # If the word is in the vocabulary, it's considered a correctly spelled word
            # Add the correctly spelled word to the list
            corrected_words.append(word)
    print(corrected_words)

    # Join the corrected words back into a string
    corrected_text = " ".join(corrected_words)

    return corrected_text
