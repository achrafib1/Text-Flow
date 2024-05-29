import re
import nltk
from nltk.tokenize import sent_tokenize


def text_processing(example, n=3):

    # convert all letters to lower case
    example = example.lower()

    # Remove links
    example = re.sub(r"http\S+|www.\S+|@|️#|!|", "", example)

    # Split the text into sentences
    sentences = sent_tokenize(example)

    # print(sentences)
    processed_text = []
    for sentence in sentences:

        # Remove other non-alphanumeric characters (excluding '<EOS>' and '.')
        sentence = re.sub(r"[^a-zA-Z0-9 .,]", " ", example)

        # Tokenize the sentence
        sentence_tokens = nltk.word_tokenize(sentence)

        #         # Replace periods with '<EOS>' token only if they are at the end of a sentence
        #         sentence_tokens = ['EOS' if token == '.' else token for token in sentence_tokens]

        #         # Add '<s>' token at the start of the text n-1 times
        #         sentence_tokens = ['<s>'] * (n-1) + sentence_tokens +['</s>']

        # Filter out empty strings
        sentence_tokens = [
            token for token in sentence_tokens if token.strip() and token
        ]

        processed_text.extend(sentence_tokens)

    return processed_text
