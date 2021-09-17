

from flask import Flask, send_from_directory,request,jsonify
from flask_cors import CORS 

from part_lookup.ebay_part_lookup import find_part_data_on_ebay

app = Flask(__name__, static_url_path='', static_folder='../hpf/build')

CORS(app)

@app.route("/api/v1/get_data")
def get_data():
    part_number = request.args.get("part_number")
    results = find_part_data_on_ebay(part_number)
    return jsonify(results)
    