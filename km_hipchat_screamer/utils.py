
from flask import jsonify
import os

class env_check(object):
    def __init__(self, env_var):
        self.env_var = env_var

    def __call__(self, f):
        def g(*args, **kwargs):
            error_message = "Not Implemented, %s not configured" % (self.env_var)
            response = jsonify(error=error_message)
            response.status_code = 501
            return response
        if os.environ.get(self.env_var):
            return f
        else:
            print "%s not supplied, %s route disabled" % (self.env_var, f.__name__)
            return g
