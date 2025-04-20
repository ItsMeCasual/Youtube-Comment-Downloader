# YouTube Comment Extractor

A simple Python script to extract top-level comments from any public YouTube video using the YouTube Data API v3. You can also filter comments by a time window from the video's publication date.

## Features

- Extract top-level comments from a specified YouTube video.
- Optionally filter comments posted within *n* minutes of video release.
- Saves the extracted data to a structured CSV file.
- Outputs comment text, username, user ID, and time since video release.


## Requirements

- Python 3.7+
- YouTube Data API v3 key


### Setup

```bash
pip install google-api-python-client
```
You will have to enter your API Key manually into the python file.


### Usage 
To download all comments from a video: 
```bash
python video_comment_extractor.py "YOUTUBE_VIDEO_LINK" 
```
To download all comments posted after n minutes of the videos release:
```bash
python video_comment_extractor.py "YOUTUBE_VIDEO_LINK" n
```
The script will create a folder "Comments" in the directory where it was executed and store the comments of each youtube video in seperate csv's. 
