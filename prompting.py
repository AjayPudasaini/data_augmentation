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
    response = client.chat.completions.create(model="gpt-4",  # 'engine' has been renamed to 'model' in the latest API
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
    output_path = os.path.join("Datas/all_datas/prompting/", os.path.basename(file))
    df.to_csv(output_path, index=False)
    
    print(f"Processed and saved: {output_path}")




