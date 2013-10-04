km-hipchat-screamer
===================

receiver of webhooks, spammer of rooms.

## Setup

    git clone git@github.com:kissmetrics/km-hipchat-screamer.git
    cd km-hipchat-screamer
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    # Assuming you have heroku's tools installed
    foreman start

## Deploy

    # Assuming you have heroku's tools installed
    heroku login
    heroku create
    git push heroku master

## Configuring

### Plugins

#### annoy

Set an environment variable for:
- `ANNOY_HIPCHAT_TOKEN`: HipChat API token (hopefully just a notifcation token)

#### statuspage

Set an environment variable for:
- `STATUSPAGE_HIPCHAT_TOKEN`: HipChat API token (hopefully just a notifcation token)
- `STATUSPAGE_NOTIFY_ROOMS`: Comma separated list of HipChat rooms to spam `1234,4321`

Optional:
- `STATUSPAGE_NOTIFY_NAME`: Name of user in HipChat room, defaults to statuspage.io
