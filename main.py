import json
import os
import psycopg2
import urllib2

from flask import abort, Flask, g, make_response, render_template, request

from lib.database import DataBase
from lib.data_source import DataSource

DATA_URL = 'https://data.sfgov.org/api/views/rqzj-sfat/rows.json?accessType=DOWNLOAD'
DATABASE_NAME = 'foodtruckfinder'
DATABASE_USER = 'root'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update({
    'DATABASE': DATABASE_NAME,
    'DATABASE_USER': DATABASE_USER
})

def init_db():
    """Initializes the database stored in app.config['DATABASE'] with data from 
    the url stored in DATA_URL"""

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
            try:
                db.add_row(
                    item['Applicant'], 
                    item['Address'], 
                    item['FoodItems'], 
                    item['Latitude'], 
                    item['Longitude']
                )
            except psycopg2.IntegrityError:
                pass

def get_db():
    """Returns a database connections, or creates one if one doesn't exist"""
    if not hasattr(g, 'db'):
        g.db = DataBase(app.config['DATABASE'], app.config['DATABASE_USER'])
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Tears down the existing database connection"""
    if hasattr(g, 'db'):
        del g.db

@app.route('/', methods=['GET'])
def index():
    """handles the '/' endpoint, returning the content of 'index.html'"""
    return render_template('index.html')

@app.route('/api/foodtrucks', methods=['GET'])
def foodtrucks():
    """handles the '/api/foodtrucks' endpoint, return a list of foodtrucks within
    the distance of the point passed as GET parameters"""
    try:
        longitude = float(request.args.get('longitude'))
        latitude = float(request.args.get('latitude'))
        distance = float(request.args.get('distance'))
    except (TypeError, ValueError):
        abort(400)

    foodtrucks = [x for x in get_db().gen_within_distance(distance, latitude, longitude)]

    return make_response(
        json.dumps(foodtrucks),
        201
    )

if __name__ == '__main__':
    app.run()
