# -*- coding: utf-8 -*-

"""
km-hipchat-screamer.statuspage
~~~~~~~~~~~~~~~~~~~~~~~

Module providing for status change alert routes the KISSmetrics HipChat Webhook service
"""


from flask import Blueprint, jsonify, request
from utils import env_check
import os
import json
import hipchat
import requests

hipchat_notification_color = { 'operational': 'green',
                               'degraded_performance': 'yellow',
                               'partial_outage': 'yellow',
                               'major_outage': 'red' }

def get_component_name(page_id, component_id):
    url = 'http://%s.statuspage.io/index.json' % (page_id)
    response = requests.get(url)
    data = response.json()
    for component in data['components']:
        if component['id'] == component_id:
            return component['name']


STATUSPAGE_HIPCHAT_TOKEN = os.environ.get('STATUSPAGE_HIPCHAT_TOKEN')
STATUSPAGE_NOTIFY_ROOMS = os.environ.get('STATUSPAGE_NOTIFY_ROOMS')

statuspage = Blueprint('statuspage', __name__)

#-------
# Routes
#-------

@statuspage.route('/statuspage/alert', methods=['POST'])
@env_check('STATUSPAGE_HIPCHAT_TOKEN')
@env_check('STATUSPAGE_NOTIFY_ROOMS')
def statuspage_route():
    """Send alerts for statuspage.io webhooks to rooms listed in STATUSPAGE_NOTIFY_ROOMS"""

    notification = json.loads(request.data)
    component_update = notification['component_update']

    component_name = get_component_name(notification['page']['id'], component_update['component_id'])

    old_status = component_update['old_status']
    new_status = component_update['new_status']
    message = "[%s] status changed from %s to %s" % (component_name, old_status, new_status)

    hipchat_api = hipchat.HipChat(token=STATUSPAGE_HIPCHAT_TOKEN)
    for channel in STATUSPAGE_NOTIFY_ROOMS.split(','):
        hipchat_api.message_room(channel, 'KM Status', message, notify=True, color=hipchat_notification_color[new_status])

    body = { "action": "message sent" }

    return jsonify(body)
