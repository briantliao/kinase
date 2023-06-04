# pip install pysrt moviepy

import os
import pysrt
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def split_video(video_file, subtitle_file, duration):
    subs = pysrt.open(subtitle_file)
    n = len(subs)
    i = 0

    while i < n:
        start_time = subs[i].start.ordinal / 1000
        if i + duration < n:
            end_time = subs[i + duration - 1].end.ordinal / 1000
        else:
            end_time = subs[n - 1].end.ordinal / 1000

        # Create new clip
        output_clip_name = "output_{}.mp4".format(i)
        ffmpeg_extract_subclip(video_file, start_time, end_time, targetname=output_clip_name)

        # Write out captions for this clip
        output_caption_name = "output_{}.srt".format(i)
        subs[i:min(i + duration, n)].save(output_caption_name, encoding='utf-8')

        i += duration

# Replace 'video.mp4' and 'subtitles.srt' with your video and SRT file
split_video('video.mp4', 'subtitles.srt', 600)  # 600 seconds = 10 minutes
