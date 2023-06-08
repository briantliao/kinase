import os

path = "videos"


def get_video_segments():
    segments = []

    # Walk through all directories starting at path
    for dirpath, _, filenames in os.walk(path):
        # Check if the current directory is a "segment" directory
        if "segment" in os.path.basename(dirpath):
            segment_video = None
            segment_transcript = None

            # Loop over all files in the current directory
            for filename in filenames:
                # Check if this file is a video or a transcript file
                # This is based on the file extension. Adjust this as needed.
                if filename.endswith(".mp4"):  # Assuming video files are .mp4
                    segment_video = os.path.join(dirpath, filename)
                elif filename.endswith(".srt"):  # Assuming transcript files are .srt
                    segment_transcript = os.path.join(dirpath, filename)

            # If both a video and transcript were found, add them to the list
            if segment_video and segment_transcript:
                segments.append((segment_video, segment_transcript))

    # Sort the list of segments by video filename and then transcript filename
    segments.sort(key=lambda x: (x[0], x[1]))
    return segments


# usage
# segments = get_video_segments()
# for segment_video, segment_transcript in segments:
# print(f"Segment video: {segment_video}")
# print(f"Segment transcript: {segment_transcript}")
