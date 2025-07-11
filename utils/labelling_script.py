import os
import google.generativeai as genai
import pandas as pd
import numpy as np
import json
from prompts import *
import time
from pprint import pprint
from typing import List


def list_video_paths(folder_path: str) -> List[str]:
    """
    List all the video paths in a directory

    Parameters
    ----------
    folder_path : str
        The path to the directory we want to get all our video files from

    Returns
    ----------
    video_paths : List[str]
        The list of videos as path strings from that directory

    Examples
    ----------
    >>> video_paths = list_video_paths("/path/to/folder")
    """
    video_paths = []
    video_extensions = ['.mp4', '.MP4']

    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return video_paths

    folder_name = os.path.basename(folder_path)

    for item_name in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item_name)

        if os.path.isfile(item_path):
            _, file_extension = os.path.splitext(item_name)
            if file_extension.lower() in video_extensions:
                video_path_format = f"{folder_name}/{item_name}"
                video_paths.append(video_path_format)

    return video_paths


def create_dataset(model: genai.GenerativeModel, folder_path: str, backup: int = -1) -> pd.DataFrame:
    """
    Create the labelled dataset

    Parameters
    ----------
    model : Any
        The generative model to use for labelling purposes
    folder_path : str
        The path to the directory we want to get all our video files from
    backup = -1 : int
        The file index from which we want to start labelling from incase the loop hits rate limits.
        Default value is -1, meaning start labelling from the first example

    Returns
    ----------
    df : pd.DataFrame
        The labelled dataset as a pandas Dataframe 

    Examples
    ----------
    Create the dataset
    >>> df = create_dataset(model, "/path/to/folder")

    In case the dataset failed after backup 40
    >>> df = create_dataset(model, "/path/to/folder", backup=41)
    """
    video_files: List[str] = []
    dataset: List[dict] = []

    video_files: str = sorted(list_video_paths(folder_path))

    print(f"Found {len(video_files)} video files:")

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
        },
    ]

    for i, video_path in enumerate(video_files):
        if backup != -1:
            if i < backup:
                continue

        filename = os.path.basename(video_path)
        print(f"\nProcessing: {filename}")
        reel = genai.upload_file(
            path=f"{folder_path}/{filename}"
        )
        time.sleep(10)

        tries = 10
        while tries > 0:
            try:
                response = model.generate_content(
                    [AUDIO_PROMPT, reel], safety_settings=safety_settings)
                response = response.text
                original_a, attack_a = response.split("\n\n")

                response = model.generate_content(
                    [VIDEO_PROMPT, reel], safety_settings=safety_settings)
                response = response.text
                original_v, attack_v = response.split("\n\n")

                response = model.generate_content(
                    [PERCEPTION_PROMPT, reel], safety_settings=safety_settings)
                response = response.text
                original_p, attack_p = response.split("\n\n")

                response = model.generate_content(
                    [DESC_PROMPT, reel], safety_settings=safety_settings)
                response = response.text
                GT, label = response.split("\n\n")

                row = {
                    "filepath": f"{folder_path}/{filename}",
                    "original_a": original_a,
                    "attack_a": attack_a,
                    "original_v": original_v,
                    "attack_v": attack_v,
                    "original_p": original_p,
                    "attack_p": attack_p,
                    "GT": GT,
                    "label": int(label.replace("\n", ""))
                }

                dataset.append(row)

                if i % 10 == 0:
                    print(f"Processed {i} files")
                    pprint(row)
                    df = pd.DataFrame(dataset)
                    df.to_csv(
                        f"../output/backup_{i}.csv", index=False
                    )

                time.sleep(10)

                break
            except:
                print("Failed. Trying again")
                tries -= 1
                time.sleep(60)

        if tries == 0:
            print("Failed to process file", filename)
            continue

    df = pd.DataFrame(dataset)

    return df


def run_labelling() -> None:
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    MODEL_NAME = "gemini-2.5-flash-preview-05-20"
    model = genai.GenerativeModel(MODEL_NAME)
    df = create_dataset(model, "<path>")
    df.to_csv("../output/final.csv", index=False)


if __name__ == "__main__":
    run_labelling()
