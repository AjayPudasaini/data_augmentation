import os
import glob
import pandas as pd
import numpy as np

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_SECRET_KEY"))

csv_dir = "Datas/all_datas/"
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))

openai_models = ["gpt-4", "gpt-3.5-turbo"] # maad add here open ai models .......

def generate_text(text, model_name, token_count=200):
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are an assistant that generates human-like text."},
            {"role": "user", "content": f"Generate paragraphs from the following prompt: {text}"}
        ],
        max_tokens=int(token_count + 20),
        temperature=0.7
    )
    generated_text = response.choices[0].message.content.strip()
    return generated_text


for file in csv_files:
    df = pd.read_csv(file)
    
    df = df.dropna(subset=["prompt"])

    for model in openai_models:
        column_name = f"{model}_generated_text"
        
        df[column_name] = df["prompt"].apply(lambda x: generate_text(x, model, len(x)))

    df.to_csv(file, index=False)

    print(f"Processed and updated: {file}")
