# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /Text-Flow
WORKDIR /Text-Flow

# Add the current directory contents into the container at /Text-Flow
ADD . /Text-Flow



# Install wget and install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y wget && \
    pip install --no-cache-dir -r requirements.txt

# Download the necessary files
RUN [ ! -f src/models/vocabulary.txt ] wget -O src/models/vocabulary.txt https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/vocabulary.txt || echo "vocabulary.txt already exists" && \
    [ ! -f src/models/unigram_counter.pkl ] wget -O src/models/unigram_counter.pkl https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/unigram_counter.pkl || echo "unigram_counter.pkl already exists" && \
    [ ! -f src/models/bigram_counter.pkl ] wget -O src/models/bigram_counter.pkl https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/bigram_counter.pkl || echo "bigram_counter.pkl already exists" && \
    [ ! -f src/models/trigram_counter.pkl ] wget -O src/models/trigram_counter.pkl https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/trigram_counter.pkl || echo "trigram_counter.pkl already exists" && \
    [ ! -f src/models/tokenizer.pkl ] wget -O src/models/tokenizer.pkl https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/tokenizer.pkl || echo "tokenizer.pkl already exists" && \
    [ ! -f src/models/ngram_counts.pkl ] wget -O src/models/ngram_counts.pkl https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/ngram_counts.pkl || echo "ngram_counts.pkl already exists" && \
    [ ! -f src/models/nplus1gram_counts.pkl ] wget -O src/models/nplus1gram_counts.pkl https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/nplus1gram_counts.pkl || echo "nplus1gram_counts.pkl already exists" && \
    [ ! -f src/models/model.h5 ] wget -O src/models/model.h5 https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/model.h5 || echo "model.h5 already exists"



# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run Streamlit app when the container launches
CMD ["streamlit", "run", "src/app.py"]
