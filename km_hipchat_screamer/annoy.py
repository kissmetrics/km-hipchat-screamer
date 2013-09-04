# -*- coding: utf-8 -*-

"""
km-hipchat-screamer.annoy
~~~~~~~~~~~~~~~~~~~~~~~

Module providing test routes for the KISSmetrics HipChat Webhook service
"""


from flask import Blueprint, jsonify
import os
import hipchat


ANNOY_HIPCHAT_TOKEN = os.environ.get('ANNOY_HIPCHAT_TOKEN')

annoy = Blueprint('annoy', __name__)

#-------
# Routes
#-------

if ANNOY_HIPCHAT_TOKEN:
    @annoy.route('/annoy/<channel>')
    def annoy_route(channel):
        """Spam a particular room"""
    
    
        hipchat_api = hipchat.HipChat(token=ANNOY_HIPCHAT_TOKEN)
        hipchat_api.message_room(channel, 'Screamer', 'test', notify=True)
    
        body = { "action": "message sent" }
    
        return jsonify(body)
else:
    print "ANNOY_HIPCHAT_TOKEN not supplied, annoy routes disabled"
