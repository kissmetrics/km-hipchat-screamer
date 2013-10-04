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
                               'major_outage': 'red',
                               'scheduled': 'gray',
                               'in_progress': 'gray',
                               'investigating': 'red',
                               'identified': 'yellow',
                               'monitoring': 'gray',
                               'resolved': 'green',
                               'postmortem': 'gray' }

def get_component_name(page_id, component_id):
    url = 'http://%s.statuspage.io/index.json' % (page_id)
    response = requests.get(url)
    data = response.json()
    for component in data['components']:
        if component['id'] == component_id:
            return component['name']


STATUSPAGE_HIPCHAT_TOKEN = os.environ.get('STATUSPAGE_HIPCHAT_TOKEN')
STATUSPAGE_NOTIFY_ROOMS = os.environ.get('STATUSPAGE_NOTIFY_ROOMS')
STATUSPAGE_NOTIFY_NAME = os.environ.get('STATUSPAGE_NOTIFY_NAME', 'statuspage.io')

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

    if 'component_update' in notification:
        page_id = notification['page']['id']
        component_update = notification['component_update']
        component_id = component_update['component_id']
        component_name = get_component_name(page_id, component_id)
        old_status = component_update['old_status']
        new_status = component_update['new_status']
        color = hipchat_notification_color[new_status]
        message = "[%s] status changed from %s to %s" % (component_name, old_status, new_status)

    elif 'incident' in notification:
        incident_update = notification['incident']
        incident_name = incident_update['name']
        incident_status = incident_update['status']
        incident_message = incident_update['incident_updates'][0]['body']
        color = hipchat_notification_color[incident_status]
        message = "[%s] %s: %s" % (incident_name, incident_status, incident_message)

    hipchat_api = hipchat.HipChat(token=STATUSPAGE_HIPCHAT_TOKEN)
    for channel in STATUSPAGE_NOTIFY_ROOMS.split(','):
        hipchat_api.message_room(channel, STATUSPAGE_NOTIFY_NAME, message, notify=True, color=color)

    body = { "action": "message sent" }

    return jsonify(body)
