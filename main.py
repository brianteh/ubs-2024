import json
from flask import Flask, jsonify, request
app = Flask(__name__)
#GET example
@app.route('/hello', methods=['GET'])
def get_employees():
 return jsonify(["Hello"])
if __name__ == '__main__':
   app.run()