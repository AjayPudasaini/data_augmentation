import random
import os
import pandas as pd
import glob
import re

# Path to your CSV directory
csv_dir = "Datas/all_datas/"

# List all CSV files in the directory
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))

def misspell_word(word):
    """Shuffle characters of a word to create a misspelling."""
    if len(word) > 3:
        middle = list(word[1:-1])
        random.shuffle(middle)
        return word[0] + ''.join(middle) + word[-1]
    elif len(word) > 1:
        return ''.join(random.sample(word, len(word)))
    return word


def misspell_paragraph(paragraph):
    """Misspell one word in each sentence of the paragraph."""
    sentences = re.split(r'(?<=[.!?]) +', paragraph)
    for i, sentence in enumerate(sentences):
        words = sentence.split()
        if words:
            # Select only one random word to misspell in each sentence
            misspell_index = random.randint(0, len(words) - 1)
            words[misspell_index] = misspell_word(words[misspell_index])
            sentences[i] = ' '.join(words)
    return ' '.join(sentences)


# paragraphs = """
#                 The quick brown fox jumps over the lazy dog. This sentence includes every letter in the alphabet. Learning to code can be challenging but rewarding. Python is a versatile programming language that many people enjoy using. Practice makes perfect when it comes to developing new skills.
#             """

# print(misspell_paragraph(paragraphs))

# Process each CSV file
for file in csv_files:
    df = pd.read_csv(file)
    
    # Drop rows where "machine_text" is NaN
    df = df.dropna(subset=["machine_text"])

    # Apply the misspell function to "machine_text" column
    df["misspell_text"] = df["machine_text"].apply(lambda x: misspell_paragraph(str(x)))

    df.to_csv(file, index=False)
    print(f"Processed and updated: {file}")
