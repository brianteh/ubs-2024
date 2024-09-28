import json
from flask import Flask, jsonify, request
app = Flask(__name__)
app.debug = True
class PrefixMiddleware(object):

    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/py')
#GET example
@app.route('/hello', methods=['GET'])
def get_employees():
 return jsonify(["Hello"])
if __name__ == '__main__':
    app.run('0.0.0.0',port=5000)