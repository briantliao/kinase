from video_dir_helper import get_video_segments
from dotenv import load_dotenv
from datetime import datetime

import ray
import time
import re
import openai
import os
import json
import sys

load_dotenv()

# Doing segmented parallelization because we are hitting rate limits
# https://platform.openai.com/account/rate-limits
# Initialize Ray
ray.init()

openai.api_key = os.environ.get("OPENAI_KEY")


def call_chatgpt_api(prompt, api_key):
    # Set the API key in the worker process
    openai.api_key = api_key

    # Send a chat completion request to the OpenAI API
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    # Introduce a delay before the next API call
    time.sleep(15)

    return completion.choices[0].message["content"]


@ray.remote
def get_video_title(tot_segment_number, segment_transcript, api_key):
    print("Processing:", tot_segment_number, segment_transcript)
    i = 0
    summaries = []

    with open(segment_transcript, "r") as f:
        lines = f.readlines()

    while i < len(lines):
        prompt = "".join(lines[i : i + 500]) + "Summarize above. Be concise."
        response = call_chatgpt_api(prompt, api_key)
        # print("Summary:", response)
        summaries.append(response)
        i += 500

    summary = "\n".join(summaries)
    prompt = (
        summary
        + "Generate a YouTube video title up to 10 words from the summaries above."
    )

    title_response = call_chatgpt_api(prompt, api_key)
    title_response = title_response.replace('"', "")
    # print("Title:", title_response)

    prompt = (
        summary
        + 'Generate YouTube video tags from the summaries above in the format: ["tag1", "tag2"]'
    )
    tags_response = call_chatgpt_api(prompt, api_key)
    try:
        tags_response = tags_response.split("]", 1)[0] + "]"
        tags_response = json.loads(tags_response)
    except json.JSONDecodeError:
        print(f"Failed to decode JSON: {tags_response} for {segment_transcript}")
    # print("Tags:", tags_response)

    prompt = summary + "Summarize above. Be concise."
    summary_response = call_chatgpt_api(prompt, api_key)
    # print("Summary:", summary_response)

    prompt = (
        "".join(lines[:500])
        + "The above is a video transcription in srt format. Give the time the speaker starts speaking. Give only the and NO other text. Use the format: 00:01:17,210."
    )
    start_time_response = call_chatgpt_api(prompt, api_key)
    try:
        # Extract the timestamp using a regular expression
        match = re.match(r"(\d{2}:\d{2}:\d{2},\d{3})", start_time_response)
        if match is None:
            raise ValueError("No valid timestamp found!")

        # Extract the timestamp and replace the comma with a period
        timestamp = match.group(1).replace(",", ".")

        # Parse the timestamp
        parsed_timestamp = datetime.strptime(timestamp, "%H:%M:%S.%f")

        match = re.search(r"segment(\d+)", segment_transcript)
        segment_number = int(match.group(1))

        # Extract the minutes and seconds
        minutes = parsed_timestamp.minute - 10 * segment_number
        seconds = parsed_timestamp.second
        start_time_response = f"{minutes:02d}:{seconds:02d}"
    except ValueError:
        print(
            f"Failed to decode time format: {start_time_response} for {segment_transcript}"
        )
    # print("Start Time:", start_time_response)

    output_name = segment_transcript.replace(".srt", ".json")
    with open(output_name, "w") as f:
        json.dump(
            {
                "title": title_response,
                "tags": tags_response,
                "summary": summary_response,
                "start_time": start_time_response,
            },
            f,
            indent=2,
        )

    print(f"Response written to {output_name}")


segments = get_video_segments()
i = 0
print("Batching 5")
if len(sys.argv) == 2:
    i = int(sys.argv[1])

while i < len(segments):
    batch = segments[i : i + 5]
    ray.get(
        [get_video_title.remote(i, segment[1], openai.api_key) for segment in batch]
    )
    time.sleep(180)
    i += 5
