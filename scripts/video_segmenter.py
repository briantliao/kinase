from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pydub import AudioSegment

import pysrt
import math
import os
import sys
os.environ["RAY_DEDUP_LOGS"] = "0"
import ray


# Initialize Ray
ray.init(num_cpus=4)

# Define a remote function with the decorator @ray.remote
# This function will be executed in parallel for each of the elements of the jobs list
@ray.remote
def slice_videos(index, video_path, srt_path, length, video_dir):
    print(f"Processing: {index}, {video_path}")
    subs = pysrt.open(srt_path)
    video = AudioSegment.from_file(video_path)

    total_seconds = len(video) / 1000  # Length of audio in seconds
    parts = math.ceil(total_seconds / length)  # Number of parts of defined length

    start = 0
    for i in range(parts):
        end = start + length
        if end > total_seconds:
            end = total_seconds

        # Create a new directory for each segment
        segment_folder = os.path.join(video_dir, f"segment{i:03d}")
        os.makedirs(segment_folder, exist_ok=True)

        # Create new clip
        output_clip_name = os.path.join(segment_folder, f"segment{i:03d}.mp4")
        ffmpeg_extract_subclip(video_path, start, end, targetname=output_clip_name)

        start_time = start * 1000  # Convert to milliseconds
        end_time = end * 1000  # Convert to milliseconds

        slice_subs = [
            s
            for s in subs
            if s.start.ordinal >= start_time and s.end.ordinal <= end_time
        ]
        # Write out captions for this clip
        output_caption_name = os.path.join(segment_folder, f"segment{i:03d}.srt")
        pysrt.SubRipFile(slice_subs).save(output_caption_name, encoding="utf-8")

        start = end


# Specify the root videos directory
root_videos_dir = "videos"

# Get all video directories in the root directory
video_dirs = sorted(
    [
        os.path.join(root_videos_dir, name)
        for name in os.listdir(root_videos_dir)
        if os.path.isdir(os.path.join(root_videos_dir, name))
    ]
)

jobs = []

for video_dir in video_dirs:
    video_file = os.path.join(video_dir, f"{os.path.basename(video_dir)}.mp4")
    subtitle_file = os.path.join(video_dir, f"{os.path.basename(video_dir)}.en.srt")

    if os.path.exists(video_file) and os.path.exists(subtitle_file):
        # Each video is segmented every 600 seconds = 10 minutes
        # Call the function with the video and subtitle file paths, and length in seconds
        jobs.append((video_file, subtitle_file, video_dir))

i = 0
if len(sys.argv) == 2:
    i = int(sys.argv[1])


# This will execute the function in parallel for each job.
results = ray.get(
    [
        slice_videos.remote(index, video_file, subtitle_file, 600, video_dir)
        for index, (video_file, subtitle_file, video_dir) in enumerate(jobs[i:], start=i)
    ]
)
