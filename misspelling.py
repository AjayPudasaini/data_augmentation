import random
import os
import random
import pandas as pd
import glob

# Path to your CSV directory
csv_dir = "Datas/all_datas/"

# List all CSV files in the directory
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))


def misspell_word(word):
    """Shuffle characters of a word to create a misspelling."""
    if len(word) > 3:
        middle = list(word[1:-1])  # Get the middle characters
        random.shuffle(middle)  # Shuffle the middle characters
        return word[0] + ''.join(middle) + word[-1]  # Rebuild the word
    elif len(word) > 1:  # Shuffle short words with 2 or 3 letters
        return ''.join(random.sample(word, len(word)))  # Shuffle all characters
    return word  # Don't change one-letter words


def misspell_paragraph(paragraph, misspell_ratio=0.7):
    """Misspell a percentage of the words in the paragraph."""
    words = paragraph.split()  # Split paragraph into words
    total_words = len(words)
    misspell_count = int(total_words * misspell_ratio)  # Calculate number of words to misspell

    # Randomly select words to misspell based on the ratio
    misspell_indices = random.sample(range(total_words), misspell_count)
    
    # Misspell words at the selected indices
    for i in misspell_indices:
        words[i] = misspell_word(words[i])
    
    # Join the words back into a paragraph
    return ' '.join(words)



# Process each CSV file
for file in csv_files:
    df = pd.read_csv(file)
    
    # Drop rows where "human_text" is NaN
    df = df.dropna(subset=["human_text"])

    # Apply the whitespace function to "human_text" column
    misspell_ratio = 0.7
    df["misspell_text"] = df["human_text"].apply(lambda x: misspell_paragraph(str(x), misspell_ratio))

    # Define output path and save the modified DataFrame
    output_path = os.path.join("Datas/all_datas/misspelling/", os.path.basename(file))
    df.to_csv(output_path, index=False)
    
    print(f"Processed and saved: {output_path}")
