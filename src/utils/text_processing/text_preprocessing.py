import re
import nltk
from nltk.tokenize import sent_tokenize
from typing import List


def text_processing(example: str, n: int = 3) -> List[str]:
    """
    The `text_processing` function cleans and tokenizes input text.
    It converts text to lower case, removes links and symbols, splits it into words, and filters out empty strings.
    It returns a list of processed tokens.

    Parameters:
    example (str): The text to be processed.
    n (int): An optional parameter with a default value of 3.

    Returns:
    List[str]: A list of processed tokens.
    """

    # Convert all letters to lower case
    example = example.lower()

    # Remove links, '@', '#', and '!' symbols
    example = re.sub(r"http\S+|www.\S+|@|️#|!|", "", example)

    # Split the text into sentences
    sentences = sent_tokenize(example)

    # print(sentences)
    processed_text = []
    for sentence in sentences:

        # Remove other non-alphanumeric characters (excluding '.')
        sentence = re.sub(r"[^a-zA-Z0-9 .,]", " ", sentence)

        # Tokenize the sentence into words
        sentence_tokens = nltk.word_tokenize(sentence)

        #         # Replace periods with '<EOS>' token only if they are at the end of a sentence
        #         sentence_tokens = ['EOS' if token == '.' else token for token in sentence_tokens]

        #         # Add '<s>' token at the start of the text n-1 times
        #         sentence_tokens = ['<s>'] * (n-1) + sentence_tokens +['</s>']

        # Filter out empty strings
        sentence_tokens = [
            token for token in sentence_tokens if token.strip() and token
        ]

        # Extend the processed text list with the tokens
        processed_text.extend(sentence_tokens)

    return processed_text
