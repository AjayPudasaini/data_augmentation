import os
import random
import pandas as pd
import glob

csv_dir = "Datas/all_datas/"
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))

# Function to randomly add a space before some commas
def add_random_space_before_comma(text, max_changes=1):
    comma_positions = [i for i, char in enumerate(text) if char == ',']
    
    # If there are no commas, return the original text
    if not comma_positions:
        return text
    
    # Determine the number of commas to modify (at most max_changes or total commas)
    num_changes = min(max_changes, len(comma_positions))
    positions_to_modify = random.sample(comma_positions, num_changes)
    
    text_list = list(text)
    for pos in sorted(positions_to_modify, reverse=True):
        text_list.insert(pos, ' ')  # Add a space before the comma
    
    return ''.join(text_list)

for file in csv_files:
    df = pd.read_csv(file)
    
    # Drop rows with NaN in "machine_text"
    df = df.dropna(subset=["machine_text"])

    # Apply the random space modification to the "machine_text" column
    df["text_with_whitespace"] = df["machine_text"].apply(
        lambda x: add_random_space_before_comma(str(x), max_changes=random.randint(1, 3))
    )

    # Save updated CSV
    df.to_csv(file, index=False)

    print(f"Processed and updated: {file}")
