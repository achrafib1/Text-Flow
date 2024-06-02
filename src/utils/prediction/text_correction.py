import numpy as np


def calculate_probability(
    word,
    unigram_counts,
    prev_word=None,
    next_word=None,
    bigram_counts=None,
    trigram_counts=None,
):
    # Calculate the individual word probability with smoothing
    word_prob = np.log(
        (unigram_counts.get(word, 0) + 1)
        / (sum(unigram_counts.values()) + len(unigram_counts))
    )

    combined_prob = word_prob

    if prev_word and bigram_counts:
        # Calculate the conditional probability of the word given the previous word with smoothing
        bigram = (prev_word, word)
        bigram_prob = np.log(
            (bigram_counts.get(bigram, 0) + 1)
            / (unigram_counts.get(prev_word, 0) + len(unigram_counts))
        )
        combined_prob = bigram_prob

    if next_word and bigram_counts:
        # Calculate the conditional probability of the word given the next word with smoothing
        bigram = (word, next_word)
        bigram_prob = np.log(
            (bigram_counts.get(bigram, 0) + 1)
            / (unigram_counts.get(next_word, 0) + len(unigram_counts))
        )
        combined_prob = bigram_prob

    if prev_word and next_word and trigram_counts:
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
