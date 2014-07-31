import json
import os
import psycopg2
import urllib2

from flask import abort, Flask, g, make_response, render_template, request
from urlparse import urlparse

from lib.database import DataBase
from lib.data_source import DataSource

DATA_URL = 'https://data.sfgov.org/api/views/rqzj-sfat/rows.json?accessType=DOWNLOAD'

app = Flask(__name__)
app.config.from_object(__name__)

url = urlparse(os.environ['DATABASE_URL'])
app.config.update({
    'PATH': url.path[1:],
    'USER': url.username,
    'PASSWORD': url.password,
    'HOST': url.hostname,
    'PORT': url.port
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
        g.db = DataBase(
            app.config['PATH'], 
            app.config['USER'],
            app.config['PASSWORD'],
            app.config['HOST'],
            app.config['PORT']
        )
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
