import os
import random
import pandas as pd
import glob

# Define a dictionary of homoglyphs
homoglyphs = {
    # Latin alphabet homoglyphs (Cyrillic/Greek/other symbols)
    'a': 'а',  # Cyrillic 'a'
    'A': 'А',  # Cyrillic 'A'
    'b': 'Ь',  # Cyrillic 'b'
    'B': 'В',  # Cyrillic 'B'
    'c': 'с',  # Cyrillic 'c'
    'C': 'С',  # Cyrillic 'C'
    'd': 'ԁ',  # Greek 'd'
    'e': 'е',  # Cyrillic 'e'
    'E': 'Е',  # Cyrillic 'E'
    'f': 'ғ',  # Cyrillic 'f'
    'g': 'ɡ',  # Greek 'g'
    'h': 'һ',  # Cyrillic 'h'
    'H': 'Н',  # Cyrillic 'H'
    'i': 'і',  # Cyrillic 'i'
    'I': 'І',  # Cyrillic 'I'
    'j': 'ј',  # Cyrillic 'j'
    'k': 'κ',  # Greek 'k'
    'K': 'К',  # Cyrillic 'K'
    'l': 'ӏ',  # Cyrillic 'l'
    'm': 'м',  # Cyrillic 'm'
    'M': 'М',  # Cyrillic 'M'
    'n': 'ո',  # Armenian 'n'
    'o': 'о',  # Cyrillic 'o'
    'O': 'О',  # Cyrillic 'O'
    'p': 'р',  # Cyrillic 'p'
    'P': 'Р',  # Cyrillic 'P'
    'q': 'ԛ',  # Greek 'q'
    'r': 'г',  # Cyrillic 'r'
    'R': 'Я',  # Cyrillic 'Ya'
    's': 'ѕ',  # Cyrillic 's'
    'S': 'Ѕ',  # Cyrillic 'S'
    't': 'т',  # Cyrillic 't'
    'T': 'Т',  # Cyrillic 'T'
    'u': 'ս',  # Armenian 'u'
    'v': 'ѵ',  # Cyrillic 'v'
    'w': 'ш',  # Cyrillic 'w'
    'W': 'Ш',  # Cyrillic 'W'
    'x': 'х',  # Cyrillic 'x'
    'X': 'Χ',  # Greek 'X'
    'y': 'у',  # Cyrillic 'y'
    'Y': 'Ү',  # Cyrillic 'Y'
    'z': 'z',  # Can remain unchanged
    'Z': 'Ζ',  # Greek 'Z'

    # Digits
    '0': 'О',  # Cyrillic 'O'
    '1': 'І',  # Cyrillic 'I'
    '3': 'З',  # Cyrillic 'Z'
    '5': 'Ѕ',  # Cyrillic 'S'
    '8': 'Ȣ',  # Cyrillic '8'

    # Special characters
    '@': 'Ѧ',  # Homoglyph-like alternative for @
    '$': 'Ƨ',  # Homoglyph for $
}


# Path to your CSV directory
csv_dir = "Datas/all_datas/"

# List all CSV files in the directory
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))

def convert_to_homoglyph(word):
    """Convert characters in a word to homoglyphs if possible."""
    new_word = []
    for char in word:
        if char in homoglyphs:
            new_word.append(homoglyphs[char])
        else:
            new_word.append(char)
    return ''.join(new_word)



def apply_homoglyphs(paragraph, ratio=0.6):
    """Convert a percentage of words in the paragraph to homoglyphs."""
    words = paragraph.split()  # Split paragraph into words
    total_words = len(words)
    
    # Ensure ratio is within a valid range
    ratio = min(max(ratio, 0), 1)
    
    convert_count = int(total_words * ratio)  # Calculate how many words to convert
    convert_count = min(convert_count, total_words)  # Ensure convert_count is not greater than total_words

    if convert_count == 0:
        return paragraph  # Return the original paragraph if no words need conversion

    # Randomly select words to convert
    indices_to_convert = random.sample(range(total_words), convert_count)

    # Convert selected words to homoglyphs
    for index in indices_to_convert:
        words[index] = convert_to_homoglyph(words[index])
    
    # Join the words back into a paragraph
    return ' '.join(words)





# Process each CSV file
for file in csv_files:
    df = pd.read_csv(file)
    
    # Drop rows where "human_text" is NaN
    df = df.dropna(subset=["human_text"])

    homoglyphs_ratio = random.randint(1, 6)
    df["text_with_homoglyph"] = df["human_text"].apply(lambda x: apply_homoglyphs(str(x), homoglyphs_ratio))

    # Define output path and save the modified DataFrame
    output_path = os.path.join("Datas/all_datas/homoglyph/", os.path.basename(file))
    df.to_csv(output_path, index=False)
    
    print(f"Processed and saved: {output_path}")
