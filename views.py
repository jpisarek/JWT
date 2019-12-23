from run import app
from flask import jsonify

@app.route('/')
def index():
    return jsonify({'message': 'The programme created for the recruitment task'})