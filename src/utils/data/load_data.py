import pickle


def load_pickle_file(file_path: str):
    with open(file_path, "rb") as f:
        return pickle.load(f)


def load_vocab(file_path: str):
    with open(file_path, "r") as f:
        return [line.strip() for line in f]
