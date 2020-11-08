<p align="center" ><strong><u>youtube-mailman</u></strong></p>

## What is this for?

youtube-mailman is a little python script for integrating YouTube to Discord Webhooks. It is totally free to use.



## How to use?

Follow these steps to start using youtube-mailman.

### Preparations

To start using youtube-mailman in your Discord server, you'll need to get the following ready:

1. A Heroku account. (Click [here](https://heroku.com) to create)
2. A Google account with Google Cloud (You don't need to set up payment method, get started [here](cloud.google.com))



### 0x00 Fork this repository

Fork this repository so you can customize it to fit your requirements later.



### 0x01 Set up a webhook in your Discord channel

In the server settings page, click [Integrations], and click [Create Webhook] under the Webhook section.![](E:\DevelopingProjects\youtube-mailman\readme-images\step-create-webhook.png)

Give the webhook a name, or give it an icon if you want. Now we are on an important step: click on [Copy Webhook URL] of your new webhook, and save the URL in a safe place. **Do NOT let others get this URL, all messages that are being sent will be using this URL.**



### 0x02 Set up Heroku app

1. After creating / logging in your Heroku account, you should be in the dashboard page. On the top-right corner, click [New] > [Create new app]. Give your app a name and select a region.

2. Then in the deploy page, click on [Connect to GitHub] button under Deploy Method section. Follow the instructions on screen to grant access to your GitHub account, then select your forked repository.

3. Switch to [Settings] tab, click [Add build pack], then choose Python from the list.

4. Switch to [Resources] tab, in the add-on search box, search for "Heroku Scheduler", then add it to your app.

5. Open the added Heroku Scheduler, select [Create job]. You should create two jobs, both of them run every hour, one starts at ":00" and another at ":30". For both jobs, enter `run python run.py`, and then save your jobs.

   > Note that you can change this settings later since the code should be modified to fit your schedule settings.



### 0x03 Set up YouTube Data API

1. Go to [Google Cloud Console](console.cloud.google.com/cloud-resource-manager), click [Create Project], and then give your project a name.
2. You'll receive a message when the project is successfully created. Go to the project page.
3. On the left menu, select [APIs & Services] > [Library], search for 'YouTube Data API', then click on it, and select [Enable].
4. Create credentials for your Discord app. For the questions of which type of credentials to create, select "YouTube Data API v3", "Other non-UI" and "Public Data". Then, the credentials is created, copy the API key and save it at a safe place.



### 0x04 Configure environment variables for Heroku app

Go to the settings tab of your Heroku app, and under the [Config Vars] section, you'll need to create the following variables:

1. `BOT_AVATAR_URL`: An URL to the image you want to use as the Webhook icon.
2. `BOT_USERNAME`: The username you want to use. Quote with double-inverted-commas (`""`) if the username contains whitespaces.
3. `CHANNELS_LIST`: A list of channels' IDs which you wish to follow. Go to [this page](https://commentpicker.com/youtube-channel-id.php) to get the channel ID. This variable uses JSON. Format:

> ```json
> {
>     "channelIDs":[
>         "first-channel-id",
>         "second-channel-id",
>         "..."
>     ]
> }
> ```

4. `MESSAGE_PATTERNS`: Patterns of Webhook messages. The pattern used is randomly picked each time. This variable uses JSON. Format:

> ```json
> {
>     "patterns":[
>         "pattern-1","pattern-2"
>     ]
> }
> ```

​	For each pattern, you should include three placeholders (`[ChannelName]`, `[VideoTitle]`, `[VideoLink]`). For instance: 

> ``` txt
> The channel "[ChannelName]" just uploaded a new video - "[VideoTitle]". Click here to watch :point_right: [VideoLink]
> ```

5. `WEBHOOK_URL`: The URL of the webhook you created.
6. `YOUTUBE_API_TOKEN`: The API key of your YouTube Data API.



### 0x05 Done! :tada:

Now you are done! Every 30 minutes, Heroku app will check for video updates, and will send a new message to your channel if new videos are found. Enjoy! 



### Limits

You have only 10000 quotas for YouTube API a day, each API request will take 100 quotas from your daily quota. Note that each time the app checks for new videos, a request to the API is performed. For example:

> You have 5 channels in your channel ID list, and video check is performed every 30 minutes. Each time the app checks for video updates, it takes away:
>
> 5 channels x 100 quotas = 500 quotas = 5 requests
>
> In half a day (12 hours), the app takes away:
>
> 12 hours x 2 x 5 requests = 120 requests
>
> Which means after half a day, you will exceed your quotas limit and the webhook will not be able to check for any video updates anymore.