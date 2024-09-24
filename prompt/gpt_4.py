import os
import glob
import pandas as pd
import numpy as np

from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()


client = OpenAI(api_key= os.getenv("OPENAI_SECRET_KEY"))

csv_dir = "Datas/all_datas/"


csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))


# List all CSV files in the directory
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))



def generate_text(text, token_count=200):
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an assistant that generate the human text."},
        {"role": "user", "content": f"Generate the paragraphs from the following prompt: {text}"}
    ],
    max_tokens=int(token_count + 20),
    temperature=0.7)

    generated_text = response.choices[0].message.content.strip()
    return generated_text



# Process each CSV file
for file in csv_files:
    df = pd.read_csv(file)
    
    # Drop rows where "human_text" is NaN
    df = df.dropna(subset=["prompt"])

    df["generated_text"] = generate_text(df["prompt"], len(df["prompt"]))

    # Define output path and save the modified DataFrame
    df.to_csv(file, index=False)

    print(f"Processed and updated: {file}")




