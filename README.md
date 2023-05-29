# Kinase: A Lecture Series to 10 Min Mini-Lecture Processing Pipeline

## Overview
This outline a robust and scalable pipeline for processing a list of YouTube videos. This includes downloading videos, segmenting them, converting to audio, generating text transcripts, and renaming and uploading these segments back to YouTube.

## Dependencies

```sh
brew install yt-dlp
brew install ffmpeg
```

`cookies.txt`, downloaded such as with [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)

## Pipeline Components
The pipeline consists of seven core components. These include:

1. **Video Downloader**
2. **Video Segmenter**
3. **Video to Audio Converter**
4. **Speech to Text Transcriber**
5. **Title Generator**
6. **Video Renamer**
7. **Video Uploader**

## Detailed Description

### 1. Video Downloader
This script receives a list of YouTube video URLs, and downloads them into a designated folder. The script must handle network errors and video access restrictions gracefully.

### 2. Video Segmenter
This script receives the folder of downloaded video files, then segments these files into 10 minute long videos. The script should be robust to videos of varying length and format.

### 3. Video to Audio Converter
This script takes in the segmented 10 minute videos and converts them into `.wav` format audio files.

### 4. Speech to Text Transcriber
This script uses a pre-trained Speech-to-Text model to generate transcripts from the `.wav` files generated in the previous step. The output of this step will be text files containing the transcript for each 10 minute segment.

### 5. Title Generator
This script uses the OpenAI Chat API to generate a suitable title for each segmented video. It takes the text transcript files generated in the previous step as input.

### 6. Video Renamer
This script takes the video titles generated in the previous step, and renames each 10 minute segment video file with the corresponding title.

### 7. Video Uploader
This script is responsible for uploading the renamed videos to YouTube. It needs to handle YouTube API interaction, including managing API quotas and errors.

## Videos File Structure

```
/videos
    |
    |--- /<video>
    |    |--- original_video
    |    |--- renamed_video
    |    |--- /segments
    |    |    |--- /<segment>
    |    |    |    |--- segment_video
    |    |    |    |--- segment_audio
    |    |    |    |--- segment_transcript
```
