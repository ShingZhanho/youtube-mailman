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
print('YouTube mailman is now working...')
reset_count = 0

while True:
    # reset_count is designed for not exceeding google cloud quota and not to trigger heroku 60 seconds error
    if reset_count != 180:
        reset_count += 1
        print("Reset count: " + str(reset_count) + " out of 180")
        utils.wait_for_ten_mins()
        continue
    else:
        print("Reached reset count, now check for videos.")
        reset_count = 0

    if last_check is None:  # wait for the first time
        last_check = time.time()
        # utils.wait_for_ten_mins()
        continue

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
            print("傳送了一條新的訊息：" + message)

            # make http request
            requests.post(os.getenv('WEBHOOK_URL'),
                          data={"username": "YouTube mailman", "avatar_url": os.getenv('BOT_AVATAR_URL'),
                                "content": message})
    last_check = time.time()
    print('A check has been performed at ' + str(last_check))
    # print(results.items[0].snippet.title)
    utils.wait_for_ten_mins()