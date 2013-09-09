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
