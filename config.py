import os
import subprocess


# Define the target directory
target_dir = "src/models"
os.makedirs(target_dir, exist_ok=True)

# URLs for the necessary files
urls = {
    "vocabulary.txt": "https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/vocabulary.txt",
    "unigram_counter.pkl": "https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/unigram_counter.pkl",
    "bigram_counter.pkl": "https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/bigram_counter.pkl",
    "trigram_counter.pkl": "https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/trigram_counter.pkl",
    "tokenizer.pkl": "https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/tokenizer.pkl",
    "ngram_counts.pkl": "https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/ngram_counts.pkl",
    "nplus1gram_counts.pkl": "https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/nplus1gram_counts.pkl",
    "model.h5": "https://github.com/achrafib1/Text-Flow/releases/download/v1.0.0/model.h5",
}

# Download the necessary files
for filename, url in urls.items():
    target_path = os.path.join(target_dir, filename)
    print(f"Downloading {filename} to {target_path} from {url}")
    subprocess.run(["wget", "-O", target_path, url], check=True)


# Install required libraries
print("Installing required libraries...")
subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

print("Setup complete. You can now run the app using 'streamlit run app.py'.")
