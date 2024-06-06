import pickle
import streamlit as st


@st.cache_data
def load_pickle_file(file_path: str):
    with open(file_path, "rb") as f:
        return pickle.load(f)


@st.cache_data
def load_vocab(file_path: str):
    with open(file_path, "r") as f:
        return [line.strip() for line in f]
