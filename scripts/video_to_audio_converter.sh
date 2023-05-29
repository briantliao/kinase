#!/bin/bash

# Path to the videos folder
VIDEO_DIR="videos"

# Iterate over each video in the directory
for video_folder in "${VIDEO_DIR}"/*; do
    if [ -d "${video_folder}" ]; then
        for segment_folder in "${video_folder}"/segment*; do
            if [ -d "${segment_folder}" ]; then
                for video_file in "${segment_folder}"/*.mp4; do
                    if [ -f "${video_file}" ]; then
                        echo "Processing: ${video_file}"

                        # Extract the base name of the video file
                        base_video_file=$(basename "${video_file}" .mp4)

                        # Convert the video to mp3
                        ffmpeg -i "${video_file}" -vn -ar 44100 -ac 2 -b:a 192k "${segment_folder}/${base_video_file}.mp3"
                    fi
                done
            fi
        done
    fi
done
