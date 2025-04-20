# Youtube Comment Extractor
import argparse
import csv
import re
import os
from datetime import datetime, timedelta
from googleapiclient.discovery import build

API_KEY = "YOUR_API_KEY" # YOUR API KEY GOES HERE


def fetch_comments(youtube, video_id):
    comments = []
    request = youtube.commentThreads().list(part = "snippet", videoId = video_id, maxResults = 100, textFormat = "plainText")

    while request:
        response = request.execute()
        for item in response.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comment_text = snippet["textDisplay"]
            user_id = snippet.get("authorChannelId", {}).get("value", "N/A")
            user_display_name = snippet.get("authorDisplayName", "N/A")
            published_at = snippet["publishedAt"]
            published_dt = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
            comments.append({
                "comment": comment_text,
                "user_id": user_id,
                "published_dt": published_dt,
                "user_display_name" : user_display_name
            })
        request = youtube.commentThreads().list_next(request, response)
    return comments

def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_video_published_date(youtube, video_id):
    response = youtube.videos().list(part = "snippet", id = video_id).execute()

    items = response.get("items",[])
    if not items: 
        return None
    published_at = items[0]["snippet"]["publishedAt"]
    return datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")

def main(API_KEY = "YOUR_API_KEY", YOUTUBE_API_SERVICE_NAME = "youtube", YOUTUBE_API_VERSION = "v3"):
    if API_KEY == "YOUR_API_KEY":
        raise NameError("You have to set your API Key manually in the python file")

    parser = argparse.ArgumentParser(description="YouTube Comment Extractor")
    parser.add_argument("video_url", type=str, help="YouTube video URL")
    parser.add_argument("time_limit", type=int, nargs="?", default=None, help="Time limit in minutes (optional)")

    args = parser.parse_args()
    video_id = extract_video_id(args.video_url)

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    video_published_date = get_video_published_date(youtube, video_id)
    comments = fetch_comments(youtube, video_id)

    if args.time_limit is not None:
        time_limit_delta = timedelta(minutes=args.time_limit)
        comments = [
            {
                "Comment": comment["comment"],
                "Username": comment["user_display_name"],
                "UserId": comment["user_id"],
                "Time": round((comment["published_dt"] - video_published_date).total_seconds() / 60)
            }
            for comment in comments
            if timedelta(0) <= (comment["published_dt"] - video_published_date) <= time_limit_delta
        ]
    else:
        comments = [
            {
                "Comment": comment["comment"],
                "Username": comment["user_display_name"],
                "UserId": comment["user_id"],
                "Time": round((comment["published_dt"] - video_published_date).total_seconds() / 60)
            }
            for comment in comments
        ]

    os.makedirs("Comments", exist_ok=True)
    csv_filename = f"Comments/{video_id}_comments.csv"
    
    fieldnames = ["Comment", "Username", "UserId", "Time"]
    with open(csv_filename, mode="w", newline='', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(comments)

    print(f"Extracted {len(comments)} comments and saved to {csv_filename}")

if __name__ == "__main__":
    main(API_KEY)

