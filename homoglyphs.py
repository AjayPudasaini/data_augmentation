import os
import random
import pandas as pd
import glob
import re

# Define a dictionary of homoglyphs
homoglyphs = {
    'a': 'а', 'A': 'А', 'b': 'Ь', 'B': 'В', 'c': 'с', 'C': 'С',
    'd': 'ԁ', 'e': 'е', 'E': 'Е', 'f': 'ғ', 'g': 'ɡ', 'h': 'һ',
    'H': 'Н', 'i': 'і', 'I': 'І', 'j': 'ј', 'k': 'κ', 'K': 'К',
    'l': 'ӏ', 'm': 'м', 'M': 'М', 'n': 'ո', 'o': 'о', 'O': 'О',
    'p': 'р', 'P': 'Р', 'q': 'ԛ', 'r': 'г', 'R': 'Я', 's': 'ѕ',
    'S': 'Ѕ', 't': 'т', 'T': 'Т', 'u': 'ս', 'v': 'ѵ', 'w': 'ш',
    'W': 'Ш', 'x': 'х', 'X': 'Χ', 'y': 'у', 'Y': 'Ү', 'z': 'z',
    'Z': 'Ζ', '0': 'О', '1': 'І', '3': 'З', '5': 'Ѕ', '8': 'Ȣ',
    '@': 'Ѧ', '$': 'Ƨ',
}

# Path to your CSV directory
csv_dir = "Datas/all_datas/"

# List all CSV files in the directory
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))

def convert_to_homoglyph(word):
    """Convert characters in a word to homoglyphs if possible."""
    new_word = []
    for char in word:
        new_word.append(homoglyphs.get(char, char))  # Replace with homoglyph if available
    return ''.join(new_word)

def apply_homoglyphs(paragraph):
    """Convert one word in each sentence of the paragraph to homoglyphs."""
    sentences = re.split(r'(?<=[.!?]) +', paragraph)  # Split paragraph into sentences
    for i, sentence in enumerate(sentences):
        words = sentence.split()
        if words:
            # Select a random word to convert to homoglyphs in each sentence
            convert_index = random.randint(0, len(words) - 1)
            words[convert_index] = convert_to_homoglyph(words[convert_index])
            sentences[i] = ' '.join(words)
    return ' '.join(sentences)


para = """
        The quick brown fox jumps over the lazy dog. 
        Artificial intelligence is transforming many industries and creating new opportunities. 
        Data science requires strong analytical skills and knowledge of programming. 
        Exploring different machine learning models can lead to better predictions and insights. 
        Python is a popular programming language for both beginners and professionals. 
        Understanding complex algorithms can be challenging but is essential for growth. 
        Collaboration and teamwork are key components in successful projects. 
        Technology evolves rapidly, so continuous learning is necessary to stay updated.
        """


# Process each CSV file
for file in csv_files:
    df = pd.read_csv(file)
    
    # Drop rows where "machine_text" is NaN
    df = df.dropna(subset=["machine_text"])

    # Apply homoglyph conversion to one word per sentence
    df["text_with_homoglyph"] = df["machine_text"].apply(lambda x: apply_homoglyphs(str(x)))

    df.to_csv(file, index=False)
    print(f"Processed and updated: {file}")
