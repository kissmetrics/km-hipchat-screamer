# -*- coding: utf-8 -*-

"""
km-hipchat-screamer.app
~~~~~~~~~~~~~~~~~~~~~~~

Module providing the application routes for the KISSmetrics HipChat Webhook service
"""


from flask import Flask, jsonify

app = Flask(__name__)


#-------
# Routes
#-------

@app.route('/')
def root_route():
    """Generate root response"""


    body = { "Title": "KISSmetrics HipChat Webhook endpoint" }

    return jsonify(body)

if __name__ == "__main__":
  app.run(debug=True)
