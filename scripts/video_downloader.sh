#!/bin/bash

# File path passed in as variable
file_path=${1:-links/links.txt}
cookies_path=${2:-cookies/cookies.txt}

text=""

# Check if the file exists
if [[ -f "$file_path" ]]; then
  # Read the file line by line
  while IFS= read -r line; do
   text+="$line"$'\n'
  done < "$file_path"
else
  echo "File not found: $file_path"
fi

yt-dlp --cookies $cookies_path -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' -o "videos/%(title)s/%(title)s.%(ext)s" $text
# experimental, must use with experiment_kinase2_youtube_transcription_split.py 
# yt-dlp --cookies $cookies_path --write-sub --sub-lang en --convert-subs srt --write-auto-sub -o "videos/%(title)s/%(title)s.srt" $text
