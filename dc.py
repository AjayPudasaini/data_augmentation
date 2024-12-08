import os
from datasets import load_dataset
import pandas as pd
import glob

csv_dir = "Datas/all_datas/"
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))

dataset = load_dataset("Hello-SimpleAI/HC3", "all")

train_data = pd.DataFrame(dataset['train'])

new_data = train_data[['question', 'human_answers', 'chatgpt_answers']].rename(
    columns={
        'question': 'prompt',
        'human_answers': 'human_text',
        'chatgpt_answers': 'machine_text'
    }
)

new_data.to_csv('Datas/all_datas/HC3.csv', index=False)