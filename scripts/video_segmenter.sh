#!/bin/bash

# Path to the videos folder
VIDEO_DIR="videos"

# Iterate over each video in the directory
for video_folder in "${VIDEO_DIR}"/*; do
    if [ -d "${video_folder}" ]; then
        for video_file in "${video_folder}"/*.mp4; do
            if [ -f "${video_file}" ]; then
                # Extract the base name of the video file
                base_video_file=$(basename "${video_file}" .mp4)

                # Skip processing if the file name is "segment"
                if [[ "${base_video_file}" == segment* ]]; then
                    echo "Skipping: ${video_file}"
                    continue
                fi

                echo "Processing: ${video_file}"

                # Split the video into 10 minute segments
                ffmpeg -i "${video_file}" -c copy -map 0 -segment_time 600 -f segment -reset_timestamps 1 "${video_folder}/segment%03d.mp4"

                # Move the segments into their own directories
                for segment_file in "${video_folder}"/segment*.mp4; do
                    base_segment_file=$(basename "${segment_file}" .mp4)
                    mkdir -p "${video_folder}/${base_segment_file}"
                    mv "${segment_file}" "${video_folder}/${base_segment_file}/${base_segment_file}.mp4"
                done
            fi
        done
    fi
done
