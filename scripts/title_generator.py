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
import random

load_dotenv()

# Not doing parallelization because we are hitting rate limits
# https://platform.openai.com/account/rate-limits
# Initialize Ray
ray.init()

openai.api_key = os.environ.get("OPENAI_KEY")


import random


def call_chatgpt_api(prompt, api_key, max_retries=5):
    # Set the API key in the worker process
    openai.api_key = api_key

    # Send a chat completion request to the OpenAI API
    retry_count = 0
    while retry_count <= max_retries:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )

            # Introduce a delay before the next API call
            if len(prompt) > 3000:
                time.sleep(3)
            elif len(prompt) > 2000:
                time.sleep(2)
            elif len(prompt) > 1000:
                time.sleep(1)

            # Successful API call, return the response
            return completion.choices[0].message["content"]

        except openai.error.RateLimitError:
            # If we're rate limited, wait and retry
            wait_time = (2**retry_count) + random.random() * 0.01
            print(
                f"Rate limit exceeded, waiting for {wait_time} seconds before retrying..."
            )
            time.sleep(wait_time)
            retry_count += 1

        except openai.Error as e:
            # For any other API errors, raise the exception
            raise e

        # If max retries reached, raise an error
        if retry_count > max_retries:
            raise Exception("Max retries reached, aborting...")


def process_srt(srt_text):
    # Split the text into lines
    lines = srt_text.split("\n")

    # Remove duplicates while preserving order
    seen = set()
    lines = [x for x in lines if not (x in seen or seen.add(x))]

    # Remove empty lines, lines with just numbers, and lines with timestamps
    processed_lines = []
    for line in lines:
        # If line is not empty and doesn't match the patterns
        if (
            line
            and not re.match(r"^\s*$", line)
            and not re.match(r"^\d+$", line)
            and not re.match(
                r"^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$", line
            )
        ):
            processed_lines.append(line)

    # Change new lines to spaces
    processed_text = "\n".join(processed_lines)
    return processed_text


@ray.remote
def get_video_title(tot_segment_number, segment_transcript, api_key):
    print("Processing:", tot_segment_number, segment_transcript)
    i = 0
    summaries = []
    tot_prompt_len = 0

    with open(segment_transcript, "r") as f:
        lines = f.readlines()

    while i < len(lines):
        parsed_lines = process_srt("".join(lines[i : i + 1000])) + "\n"
        prompt = parsed_lines + "Summarize above. Be concise."
        tot_prompt_len += len(prompt)
        response = call_chatgpt_api(prompt, api_key)
        # print("Summary:", response)
        summaries.append(response)
        i += 1000

    summary = "\n".join(summaries) + "\n"
    prompt = (
        summary
        + "Generate a YouTube video title up to 10 words from the summaries above."
    )
    tot_prompt_len += len(prompt)
    title_response = call_chatgpt_api(prompt, api_key)
    title_response = title_response.replace('"', "")
    # print("Title:", title_response)

    prompt = (
        summary
        + 'Generate YouTube video tags from the summaries. Do NOT include "YouTube video" or "YouTube video tags".\n'
        + 'Format: ["tag1", "tag2"]'
    )
    tot_prompt_len += len(prompt)
    tags_response = call_chatgpt_api(prompt, api_key)
    try:
        tags_response = tags_response.split("]", 1)[0] + "]"
        tags_response = json.loads(tags_response)
    except json.JSONDecodeError:
        print(f"Failed to decode JSON: {tags_response} for {segment_transcript}")
    # print("Tags:", tags_response)

    prompt = summary + "Summarize above. Be concise."
    tot_prompt_len += len(prompt)
    summary_response = call_chatgpt_api(prompt, api_key)
    # print("Summary:", summary_response)

    prompt = (
        "".join(lines[:100])
        + "The above is a video transcription in srt format. Give the time the speaker starts speaking. "
        + "Give only the time and NO other text. Use the format: 00:01:17,210."
    )
    tot_prompt_len += len(prompt)
    start_time_response = call_chatgpt_api(prompt, api_key)
    try:
        match_time = re.search(r"\d{2}:\d{2}:\d{2},\d{3}", start_time_response)
        timestamp = match_time.group()
        _, minute, seconds_millisec = timestamp.split(":")
        seconds, _ = seconds_millisec.split(",")

        # Convert minute and second to integers
        minute = int(minute)
        seconds = int(seconds)

        match_segment = re.search(r"segment(\d+)", segment_transcript)
        segment_number = int(match_segment.group(1))

        # Extract the minutes and seconds
        minutes = minute - 10 * segment_number
        seconds = seconds
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

    if tot_prompt_len > 25000:
        time.sleep(25)
    elif tot_prompt_len > 20000:
        time.sleep(20)
    elif tot_prompt_len > 15000:
        time.sleep(15)
    elif tot_prompt_len > 10000:
        time.sleep(10)
    elif tot_prompt_len > 5000:
        time.sleep(5)


segments = get_video_segments()
i = 0
if len(sys.argv) == 2:
    i = int(sys.argv[1])

ray.get(
    [
        get_video_title.remote(index, segment[1], openai.api_key)
        for index, segment in enumerate(segments[i:], start=i)
    ]
)

# for j in range(i, len(segments)):
#     segment = segments[j]
#     tot_prompt_len = get_video_title(j, segment[1], openai.api_key)
