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

yt-dlp --cookies $cookies_path --write-sub --sub-lang en --convert-subs srt --write-auto-sub --skip-download -o "videos/%(title)s/%(title)s" $text
