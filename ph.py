from parrot import Parrot
import torch
import warnings
warnings.filterwarnings("ignore")

import os
import random
import pandas as pd
import glob

csv_dir = "Datas/all_datas/"
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))


parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5")
def paraphrase(text):
  para_phrases = parrot.augment(input_phrase=text, use_gpu=False)
  try:
    paraphrased_text = para_phrases[0][0]
  except:
    paraphrased_text = text
  return paraphrased_text
result = paraphrase("The quick brown fox jumps over a lazy dog.")

print(result)


# Process each CSV file
for file in csv_files:
    df = pd.read_csv(file)
    
    # Drop rows where "machine_text" is NaN
    df = df.dropna(subset=["machine_text"])

    # Apply the whitespace function to "machine_text" column
    df["pharaphrased_text"] = df["machine_text"].apply(lambda x: paraphrase(str(x)))

    df.to_csv(file, index=False)

    print(f"Processed and updated: {file}")
