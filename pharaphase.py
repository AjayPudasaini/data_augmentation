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

def paraphrase_text(text, token_count=200):
    response = client.chat.completions.create(model="gpt-4",  # 'engine' has been renamed to 'model' in the latest API
    messages=[
        {"role": "system", "content": "You are an assistant that paraphrases text."},
        {"role": "user", "content": f"Paraphrase the following text: {text}"}
    ],
    max_tokens=int(token_count + 20),
    temperature=0.7)

    # Extract the paraphrased text
    paraphrased_text = response.choices[0].message.content.strip()
    return paraphrased_text



# Process each CSV file
for file in csv_files:
    df = pd.read_csv(file)
    
    df = df.dropna(subset=["machine_text"])

    df["pharaphase_text"] = paraphrase_text(df["machine_text"], len(df["human_text"]))

    df.to_csv(file, index=False)

    print(f"Processed and updated: {file}")




