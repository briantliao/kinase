from video_dir_helper import get_video_segments
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import sys
import json
import random
import time


def exponential_backoff(func):
    def wrapper(*args, **kwargs):
        for n in range(5):
            try:
                return func(*args, **kwargs)
            except HttpError as e:
                sleep_time = (2**n) + random.random()
                print(f"HTTP error: {e}. Retrying in {sleep_time} seconds")
                time.sleep(sleep_time)
        raise Exception("Failed after 5 retries")

    return wrapper


def authenticate():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    scopes = [
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.force-ssl",
    ]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes
    )
    credentials = flow.run_local_server(port=0)
    return credentials


@exponential_backoff
def upload_video(credentials, filename, title, description, tags):
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",
                "description": description,
                "title": title,
                "tags": tags,
            },
            "status": {
                "privacyStatus": "unlisted",
                "selfDeclaredMadeForKids": False,
            },
        },
        media_body=MediaFileUpload(filename),
    )
    response = request.execute()

    return response["id"]


@exponential_backoff
def add_video_to_playlist(credentials, video_id, playlist_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        },
    )
    response = request.execute()

    return response["id"]


def process_segment(i, segment_file, playlist_id, pre_title):
    print(f"Processing {i}, {segment_file}")

    segment_metadata_file = segment_file.replace(".mp4", ".json")
    metadata = None
    with open(segment_metadata_file, "r") as f:
        metadata = json.load(f)
    # Upload a video and add it to a playlist
    video_id = upload_video(
        credentials,
        segment_file,
        pre_title + ": " + metadata["title"].replace(":", " -"),
        "Starts at " + metadata["start_time"] + "\n" + metadata["summary"],
        metadata["tags"],
    )
    print(f"{segment_file} uploaded to YouTube")

    add_video_to_playlist(credentials, video_id, playlist_id)
    print(
        f"{segment_file} added to playlist: https://www.youtube.com/playlist?list={playlist_id}"
    )


segments = get_video_segments()
if len(sys.argv) != 4:
    print(
        "Please pass the command as follows: python scripts/video_uploader.py <playlist_id> <pre_title> <index of first video>"
    )
    exit()

# Perform OAuth flow and get credentials
credentials = authenticate()

# currently YouTube has a limit of 6 videos per day...

playlist_id = sys.argv[1]
pre_title = sys.argv[2]
i = int(sys.argv[3])
# Execute Serially
for index, segment in enumerate(segments[i : i + 6], start=i):
    process_segment(index, segment[0], playlist_id, pre_title)
