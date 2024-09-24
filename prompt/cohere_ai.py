import os
import glob
import pandas as pd
import cohere

from dotenv import load_dotenv

load_dotenv()

cohere_client = cohere.Client(api_key=os.getenv("COHERE_SECRET_KEY"))


csv_dir = "Datas/all_datas/"
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))

cohere_models = ["command-xlarge-nightly"] # maad add here cohere ai models.......

def generate_cohere_text(text, model_name, token_count=200):
    response = cohere_client.generate(
        model=model_name,
        prompt=text,
        max_tokens=token_count + 20,
        temperature=0.7
    )
    return response.generations[0].text.strip()

# prompt = """Write a short story about an astronaut who discovers a new planet inhabited by intelligent life. The astronaut must decide whether to make contact or return home without revealing the discovery."
# """
# data = generate_cohere_text(prompt, model_name="command-xlarge-nightly", token_count=200)
# print("data", data)

for file in csv_files:
    df = pd.read_csv(file)
    
    # Drop rows where "prompt" is NaN
    df = df.dropna(subset=["prompt"])

    for model in cohere_models:
        column_name = f"{model}_generated_text"
        df[column_name] = df["prompt"].apply(lambda x: generate_cohere_text(x, model, len(x)))

    df.to_csv(file, index=False)

    print(f"Processed and updated: {file}")

