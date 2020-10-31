import os
import pyyoutube
import time
import datetime
import requests
import utils
import json
import random

api = pyyoutube.Api(api_key=os.getenv('YOUTUBE_API_TOKEN'))  # initializes a new api object
last_check = datetime.datetime.timestamp(datetime.datetime.now() - datetime.timedelta(hours=1))
print('YouTube mailman starts')

# gets the list of channels to check
channelIDs = json.loads(os.getenv('CHANNELS_LIST'))
for channel in channelIDs['channelIDs']:
    try:
        results = api.search(parts='snippet', channel_id=channel, order='date')
    except pyyoutube.PyYouTubeException:
        print('An error occurred while getting videos')
        break

    # get latest video and compare
    video_upload_time = time.mktime(datetime.datetime.strptime(
        results.items[0].snippet.publishedAt, '%Y-%m-%dT%H:%M:%SZ').timetuple())

    if video_upload_time > last_check:  # new video since last check
        # get a pattern for message
        patterns = json.loads(os.getenv('MESSAGE_PATTERNS'))
        chosen_pattern = str(patterns['patterns'][random.randint(0, len(patterns['patterns']) - 1)])

        # get video info
        channel_title = results.items[0].snippet.channelTitle
        video_title = results.items[0].snippet.title
        video_link = 'https://youtu.be/' + results.items[0].id.videoId

        # generate the message
        message = chosen_pattern.replace('[ChannelName]', channel_title) \
            .replace('[VideoTitle]', video_title) \
            .replace('[VideoLink]', video_link)
        print("A message was sent: " + message)

        # make http request
        requests.post(os.getenv('WEBHOOK_URL'),
                      data={"username": "YouTube mailman", "avatar_url": os.getenv('BOT_AVATAR_URL'),
                            "content": message})
print('A check has been performed at ' + str(datetime.datetime.now()))
# print(results.items[0].snippet.title)
