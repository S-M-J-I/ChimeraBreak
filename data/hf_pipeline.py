from datasets import Dataset, DatasetDict, Image, Audio, Value, Features
import pandas as pd
from huggingface_hub import HfApi
import os
import time

df = pd.read_csv("./dataset.csv")

data = []
for idx, row in df.iterrows():
    filepath = row['filepath']
    entry = {
        'filepath': filepath,
        'original_a': row['original_a'],
        'attack_a': row['attack_a'],
        'original_v': row['original_v'],
        'attack_v': row['attack_v'],
        'original_p': row['original_p'],
        'attack_p': row['attack_p'],
        'GT': row['GT'],
        'label': int(row['label']),
    }

    data.append(entry)

features = Features({
    'filepath': Value('string'),
    'original_a': Value('string'),
    'attack_a': Value('string'),
    'original_v': Value('string'),
    'attack_v': Value('string'),
    'original_p': Value('string'),
    'attack_p': Value('string'),
    'GT': Value('string'),
    'label': Value('int64'),
})


dataset = Dataset.from_list(data, features=features)


dataset.push_to_hub(
    "smji/SVMA-dataset",
    private=True,
)

api = HfApi()

start = False

for i, video_file in enumerate(os.listdir("videos")):

    if video_file == "v72.mp4":
        start = True
        continue

    if start and video_file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        api.upload_file(
            path_or_fileobj=os.path.join("videos", video_file),
            path_in_repo=f"videos/{video_file}",
            repo_id="smji/SVMA-dataset",
            repo_type="dataset"
        )
        print("Uploaded", video_file)
        time.sleep(30)
