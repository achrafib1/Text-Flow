import pickle
import streamlit as st
from typing import List, Any


@st.cache_data
def load_pickle_file(file_path: str) -> Any:
    """
    Loads a pickle file from the given file path.

    Parameters:
    file_path (str): The path to the pickle file.

    Returns:
    Any: The data loaded from the pickle file.
    """
    with open(file_path, "rb") as f:
        return pickle.load(f)


@st.cache_data
def load_vocab(file_path: str) -> List[str]:
    """
    Loads a vocabulary from a file. Each line in the file is considered a word in the vocabulary.

    Parameters:
    file_path (str): The path to the file containing the vocabulary.

    Returns:
    List[str]: The list of words in the vocabulary.
    """
    with open(file_path, "r") as f:
        return [line.strip() for line in f]
