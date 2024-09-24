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
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))

def replace_with_synonyms(paragraph, max_tokens=500):
    prompt = f"Replace words in the following paragraph with synonyms, while maintaining the original meaning: \"{paragraph}\""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens= int(max_tokens + 100),
        temperature=0.7
    )

    synonym_replaced_paragraph = response.choices[0].message.content.strip()
    return synonym_replaced_paragraph


for file in csv_files:
    df = pd.read_csv(file)
    
    df = df.dropna(subset=["prompt"])

    df["synonym_replaced"] = replace_with_synonyms(df["prompt"], len(df["prompt"]))

    df.to_csv(file, index=False)
    
    print(f"Processed and updated: {file}")



