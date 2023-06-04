#!/bin/bash

# Path to videos directory
videos_path="videos"

# Find files named like "segment000.wav", "segment001.wav", etc, and echo each one sorted
while IFS= read -r file; do
    ./whisper/whisper\.cpp/main -m "./whisper/whisper.cpp/models/ggml-base.en.bin" -olrc "$file"

done < <(find "$videos_path" -type f -name "segment[0-9][0-9][0-9].wav" | sort)