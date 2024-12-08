import os
import random
import pandas as pd
import glob

# Path to your CSV directory
csv_dir = "Datas/all_datas/"

# List all CSV files in the directory
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))

def remove_random_articles(paragraph, percentage=20):
    # List of articles to potentially remove
    articles = ['a', 'an', 'the']
    
    # Split the paragraph into words and identify indices of articles
    words = paragraph.split()
    article_indices = [i for i, word in enumerate(words) if word.lower() in articles]
    
    # Calculate the number of articles to remove
    num_to_remove = max(1, int(len(article_indices) * (percentage / 100)))
    
    # Randomly select indices of articles to remove
    indices_to_remove = random.sample(article_indices, min(num_to_remove, len(article_indices)))
    
    # Create a new list of words excluding the selected articles
    words_without_articles = [
        word for i, word in enumerate(words) if i not in indices_to_remove
    ]
    
    # Join the words back into a paragraph
    return ' '.join(words_without_articles)

# Process each CSV file
for file in csv_files:
    df = pd.read_csv(file)
    
    # Drop rows where "machine_text" is NaN
    df = df.dropna(subset=["machine_text"])

    # Apply the article removal function to the "machine_text" column
    df["text_with_removed_articles"] = df["machine_text"].apply(
        lambda x: remove_random_articles(str(x), percentage=20)
    )

    # Save the modified DataFrame back to the original file
    df.to_csv(file, index=False)

    print(f"Processed and updated: {file}")
