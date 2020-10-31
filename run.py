import os
import pyyoutube
import time
import datetime
import requests
import utils
import json
import random

api = pyyoutube.Api(api_key=os.getenv('YOUTUBE_API_TOKEN'))  # initializes a new api object
last_check = None

while True:
    if last_check is None:  # wait for the first time
        last_check = time.time()
        # utils.wait_for_ten_mins()
        continue

    # gets the list of channels to check
    channelIDs = json.loads(os.getenv('CHANNELS_LIST'))
    for channel in channelIDs['channelIDs']:
        results = api.search(parts='snippet', channel_id=channel, order='date')

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
            message = chosen_pattern.replace('[ChannelName]', channel_title)\
                .replace('[VideoTitle]', video_title)\
                .replace('[VideoLink]', video_link)
            print("傳送了一條新的訊息：" + message)

            # make http request
            requests.post(os.getenv('WEBHOOK_URL'),
                          data={"username": "YouTube mailman",
                                "avatar_url": os.getenv('BOT_AVATAR_URL'),
                                "content": message})
        else:
            print("在" + str(time.time()) + "進行了檢查，沒有發現新影片。")
        last_check = time.time()
        # print(results.items[0].snippet.title)
    utils.wait_for_ten_mins()
