# Kinase: A Lecture Series to 10 Min Mini-Lecture Processing Pipeline

![](riboflavin_kinase.png)

[Source](https://commons.wikimedia.org/wiki/File:Riboflavin_kinase.png)

## Dependencies

```sh
brew install yt-dlp
brew install ffmpeg
```

`cookies.txt`, downloaded such as with [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)

Python 3.10 until [Ray](https://www.ray.io/) library updates to Python 3.11 or later

## Videos File Structure

```
/videos
    |
    |--- /<video>
    |    |--- original_video
    |    |--- renamed_video
    |    |--- /segment
    |    |    |--- segment_video
    |    |    |--- segment_audio
    |    |    |--- segment_transcript
    |    |--- /segment
    |    |    |--- segment_video
    |    |    |--- segment_audio
    |    |    |--- segment_transcript
    |--- /<video>
    |    |--- original_video
    |    |--- renamed_video
    |    |--- /segment
    |    |    |--- segment_video
    |    |    |--- segment_audio
    |    |    |--- segment_transcript
    |    |--- /segment
    |    |    |--- segment_video
    |    |    |--- segment_audio
    |    |    |--- segment_transcript
```
