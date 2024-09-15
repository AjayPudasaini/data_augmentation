import os
import random
import pandas as pd
import glob

import openai


# Path to your CSV directory
csv_dir = "Datas/all_datas/"

# List all CSV files in the directory
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))


# Function to generate context-based substitutions using OpenAI GPT
def openai_substitution(text):
    response = openai.Completion.create(
        engine="gpt-4",  # Use GPT-4 or another available engine
        prompt=f"Replace 60% of the words in the following paragraph with contextually appropriate synonyms while preserving the meaning:\n\n{text}",
        max_tokens=200,
        temperature=0.7
    )
    
    return response.choices[0].text.strip()


# Process each CSV file
for file in csv_files:
    df = pd.read_csv(file)
    
    # Drop rows where "human_text" is NaN
    df = df.dropna(subset=["human_text"])

    df["text_with_sico"] = df["human_text"].apply(lambda x: openai_substitution(str(x)))

    # Define output path and save the modified DataFrame
    output_path = os.path.join("Datas/all_datas/sico/", os.path.basename(file))
    df.to_csv(output_path, index=False)
    
    print(f"Processed and saved: {output_path}")