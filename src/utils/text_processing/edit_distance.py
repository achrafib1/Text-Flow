import numpy as np
from typing import Set


def edits1(word: str) -> Set[str]:
    """
    Generates all strings that are one edit away from the input word.

    Parameters:
    word (str): The word to be edited.

    Returns:
    Set[str]: A set of words that are one edit away from the input word.
    """
    letters = "abcdefghijklmnopqrstuvwxyz"
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word: str) -> Set[str]:
    """
    Generates all strings that are two edits away from the input word.

    Parameters:
    word (str): The word to be edited.

    Returns:
    Set[str]: A set of words that are two edits away from the input word.
    """
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))


def edits3(word: str) -> Set[str]:
    """
    Generates all strings that are three edits away from the input word.

    Parameters:
    word (str): The word to be edited.

    Returns:
    Set[str]: A set of words that are three edits away from the input word.
    """
    return set(e3 for e1 in edits1(word) for e2 in edits1(e1) for e3 in edits1(e2))
