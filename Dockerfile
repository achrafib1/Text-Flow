# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /Text-Flow
WORKDIR /Text-Flow

# Add the current directory contents into the container at /Text-Flow
ADD . /Text-Flow



# Install wget
RUN apt-get update && apt-get install -y wget

# Download the necessary files
RUN wget -O src/models/vocabulary.txt https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/vocabulary.txt && \
    wget -O src/models/unigram_counter.pkl https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/unigram_counter.pkl && \
    wget -O src/models/bigram_counter.pkl https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/bigram_counter.pkl && \
    wget -O src/models/trigram_counter.pkl https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/trigram_counter.pkl && \
    wget -O src/models/tokenizer.pkl https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/tokenizer.pkl && \
    wget -O src/models/ngram_counts.pkl https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/ngram_counts.pkll && \
    wget -O src/models/nplus1gram_counts.pkl https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/nplus1gram_counts.pkl && \
    wget -O src/models/model.h5 https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/model.h5

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run Streamlit app when the container launches
CMD ["streamlit", "run", "src/app.py"]
