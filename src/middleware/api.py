from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from logic import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

logic = Logic()

@app.route('/')
@cross_origin()
def index():
    return "Server Connected"

@app.route('/outlets/brand/<string:brand_name>', methods=["GET"])
@cross_origin()
def outlets_brand(brand_name):
    outlets = logic.get_outlet_by_brand(brand_name)
    return outlets

@app.route('/outlets/source/<string:source_name>', methods=["GET"])
@cross_origin()
def outlets_source(source_name):
    outlets = logic.get_outlet_by_source(source_name)
    return outlets

@app.route('/menus/price/above/<string:price>', methods=["GET"])
@cross_origin()
def menus_price(price):
    menus = logic.get_menu_item_by_price(price)
    return menus

@app.route('/insert/outlet/', methods=["POST"])
@cross_origin()
def post_outlet():
    if request.method == 'POST':
        get_data=request.args
        logic.create_outlet(get_data.to_dict())

    return 'insert successfully'
