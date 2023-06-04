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
                        output_file="${segment_folder}/${base_video_file}.wav"

                        # Convert the video to wav
                        if [ ! -f "$output_file" ]; then
                            ffmpeg -i "${video_file}" -vn -ar 16000 -ac 2 "$output_file"
                        else
                            echo "File $output_file already exists."
                        fi
                    fi
                done
            fi
        done
    fi
done
