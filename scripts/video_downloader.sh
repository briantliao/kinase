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

# default is yt-dlp -f "bv+ba/b" best video/audio merged
yt-dlp --cookies $cookies_path -S "+size,+br" -o "videos/%(title)s/%(title)s.%(ext)s" $text