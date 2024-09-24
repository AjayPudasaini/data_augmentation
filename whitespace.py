import os
import random
import pandas as pd
import glob

csv_dir = "Datas/all_datas/"
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))

def add_random_whitespace(paragraph, max_spaces=3):
    def insert_spaces(word):
        if len(word) < 2:
            return word
        word_list = list(word)
        num_inserts = random.randint(1, max_spaces)
        for _ in range(num_inserts):
            pos = random.randint(0, len(word_list) - 1)
            word_list.insert(pos, ' ')
        return ''.join(word_list)
    
    words = paragraph.split()
    new_words = []
    
    for word in words:
        new_word = insert_spaces(word)
        new_words.append(new_word)
        
        spaces_to_add = random.randint(0, max_spaces)
        if spaces_to_add > 0:
            new_words.append(' ' * 2)
    
    new_paragraph = ''.join(new_words)
    return new_paragraph



for file in csv_files:
    df = pd.read_csv(file)
    
    df = df.dropna(subset=["machine_text"])

    max_space = random.randint(1, 6)
    df["text_with_whitespace"] = df["machine_text"].apply(lambda x: add_random_whitespace(str(x), max_space))

    df.to_csv(file, index=False)

    print(f"Processed and updated: {file}")

