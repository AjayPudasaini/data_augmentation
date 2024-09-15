import os
import random
import pandas as pd
import glob

# Path to your CSV directory
csv_dir = "Datas/all_datas/"

# List all CSV files in the directory
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))


def remove_articles(paragraph):
    # List of articles to remove
    articles = ['a', 'an', 'the']
    
    # Split the paragraph into words
    words = paragraph.split()
    
    # Remove words that are in the articles list
    words_without_articles = [word for word in words if word.lower() not in articles]
    
    # Join the words back into a paragraph
    return ' '.join(words_without_articles)

# Process each CSV file
for file in csv_files:
    df = pd.read_csv(file)
    
    # Drop rows where "human_text" is NaN
    df = df.dropna(subset=["human_text"])

    # Apply the whitespace function to "human_text" column
    max_space = random.randint(1, 6)
    df["text_with_removed_articles"] = df["human_text"].apply(lambda x: remove_articles(str(x)))

    # Define output path and save the modified DataFrame
    output_path = os.path.join("Datas/all_datas/removed_articles/", os.path.basename(file))
    df.to_csv(output_path, index=False)
    
    print(f"Processed and saved: {output_path}")
