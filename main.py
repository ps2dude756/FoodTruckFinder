import json
import os
import urllib2

from flask import abort, Flask, g, make_response, render_template, request

from lib.database import DataBase
from lib.data_source import DataSource

DATA_URL = 'https://data.sfgov.org/api/views/rqzj-sfat/rows.json?accessType=DOWNLOAD'
DATABASE_NAME = 'foodtrucks.db'

app = Flask(__name__)

def init_db():
    with app.app_context():
        data = json.loads(urllib2.urlopen(DATA_URL).read())
        ds = DataSource(data['data'], data['meta']['view']['columns'])
        headers = ds.get_headers(
            set([
                'Applicant', 
                'Address', 
                'FoodItems', 
                'Latitude', 
                'Longitude'
            ]),
            'name'
        )
        db = get_db()
        db.init_database()
        for item in ds.gen_items(headers):
            db.add_row(
                item['Applicant'], 
                item['Address'], 
                item['FoodItems'], 
                item['Latitude'], 
                item['Longitude']
            )

def get_db():
    if not hasattr(g, 'db'):
        g.db = DataBase(DATABASE_NAME)
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        del g.db

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/foodtrucks', methods=['GET'])
def foodtrucks():
    try:
        longitude = float(request.args.get('longitude'))
        latitude = float(request.args.get('latitude'))
        distance = float(request.args.get('distance'))
    except TypeError:
        abort(400)

    foodtrucks = [x for x in get_db().gen_within_distance(distance, latitude, longitude)]

    return make_response(
        json.dumps(foodtrucks),
        201
    )

if __name__ == '__main__':
    app.run()
