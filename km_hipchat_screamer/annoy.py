# -*- coding: utf-8 -*-

"""
km-hipchat-screamer.annoy
~~~~~~~~~~~~~~~~~~~~~~~

Module providing test routes for the KISSmetrics HipChat Webhook service
"""


from flask import Blueprint, jsonify
from utils import env_check
import os
import hipchat


ANNOY_HIPCHAT_TOKEN = os.environ.get('ANNOY_HIPCHAT_TOKEN')

annoy = Blueprint('annoy', __name__)

#-------
# Routes
#-------

@annoy.route('/annoy/<channel>')
@env_check('ANNOY_HIPCHAT_TOKEN')
def annoy_route(channel):
    """Spam a particular room"""


    hipchat_api = hipchat.HipChat(token=ANNOY_HIPCHAT_TOKEN)
    hipchat_api.message_room(channel, 'Screamer', 'test', notify=True)

    body = { "action": "message sent" }

    return jsonify(body)
