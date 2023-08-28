import os
import re
from googleapiclient.discovery import build
from datetime import timedelta
from dotenv import load_dotenv

#load the stored environments
load_dotenv()

yt_api_credentials =os.environ.get('YOUTUBE_API')


youtube = build('youtube', 'v3', developerKey=yt_api_credentials)


# channel details and stats
# request = youtube.channels().list(
#     part ='contentDetails, statistics',
#     forUsername='schafer5'  #tutorial from this guy
# )
# response = request.execute()
# print(response)


#playlists from a channel
playlist_request = youtube.playlists().list(
    part ='contentDetails, snippet',
    channelId ="UCCORR0h7IVbG5-A4b_p79XQ" #my channel ID
)

playlist_response = playlist_request.execute()


# request = youtube.comments().list(
#         part="snippet",
#         parentId="UgzDE2tasfmrYLyNkGt4AaABAg"
#     )
# response = request.execute()

# kind = response['kind']
# print(response)



#The code for getting total time for a playlist
hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

total_seconds = 0
count = 0
nextPageToken = None

while False:
    #items of a playlist --> first five of the videos
    playlist_requestItem = youtube.playlistItems().list(
        part ='contentDetails, snippet',
        # playlistId ="PL5pMjciGr70uZ1_VONtIzxbFWzGnKzol7",  #playlist for huberman podcast
        playlistId ="PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU",
        # playlistId ="PL-wATfeyAMNqIee7cH3q1bh4QJFAaeNv0",
        maxResults=50,
        pageToken=nextPageToken
    )

    playlist_response = playlist_requestItem.execute()

    vid_ids = []
    for item in playlist_response['items']:
        vid_ids.append(item['contentDetails']['videoId'])

    # print(','.join(vid_ids))

    vid_request = youtube.videos().list(
        part ="contentDetails",
        id=','.join(vid_ids)
    )

    vid_response = vid_request.execute()

    for item in  vid_response['items']:
        duration = item['contentDetails']['duration']
        
        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)

        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        # print(hours, minutes, seconds)
        count += 1
        video_seconds = timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds
        ).total_seconds()

        total_seconds += video_seconds

    #next page of the playlist if there are any
    nextPageToken = playlist_response.get('nextPageToken')
    #if no more pages to fetch then breakout of the loop
    if not nextPageToken:
        break



total_seconds = int(total_seconds)
print(count, total_seconds)

minutes, seconds = divmod(total_seconds, 60)
hours, minutes = divmod(minutes, 60)

print("Total duration of the playlist",f'{hours}:{minutes}:{seconds}')
print(playlist_response)


youtube.close()