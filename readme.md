# Home Security

**Home Security** allows you to automatically detect strangers in the video.

![Imgur](https://i.imgur.com/Wmvv9yV.png)

## About

* Different input sources: 
    * camera by id
    * file
    * URL
* Adding trusted persons to the database. Faces detected in the video will be compared with them later.
* Disabling processing pipeline steps
* Notifications via e-mail (GMail only) or Telegram (`@alarmer_bot`)

## Setup
Requirments stores in `req.txt`.

Settings stored in folder `Configuration`

* `camera_config.json`
    * `fps` - how quickly the source will be read
    * `cameras` - list of cameras
        * `name` - name for log
        * `source` - port or path
* `notification_config.json` 
    * `password` - application key for GMail
    * `bot_key` - API-KEY bot `@alarmer_bot`
