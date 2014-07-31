import psycopg2

MILES = """
    create or replace function 
    miles(kilometers double precision) 
    returns double precision
    as 'select 0.621371*kilometers;'
    language sql
"""
HAVERSINE_FUNCTION = """
    create or replace function 
    haversine_function(theta1 double precision, theta2 double precision) 
    returns double precision
    as 'select power(sin((theta2-theta1)/2.0), 2.0);'
    language sql
"""
HAVERSINE_FORMULA = """
    create or replace function 
    haversine_formula(
        latitude1 double precision, 
        longitude1 double precision, 
        latitude2 double precision, 
        longitude2 double precision
    ) returns double precision
    as 'select haversine_function(latitude1, latitude2) + 
    cos(latitude1)*cos(latitude2)*
    haversine_function(longitude1, longitude2);'
    language sql
"""
GREAT_CIRCLE_DISTANCE = """
    create or replace function 
    great_circle_distance(
        latitude1 double precision, 
        longitude1 double precision, 
        latitude2 double precision, 
        longitude2 double precision
    ) returns double precision
    as 'select 2*6371.0*asin(sqrt(
        haversine_formula(latitude1, longitude1, latitude2, longitude2)
    ));'
    language sql
"""

class DataBase:
    def __init__(self, database, user, password, host, port):
        self.conn = psycopg2.connect(
            database=database, 
            user=user,
            password=password,
            host=host,
            port=port
        )

    def __del__(self):
        self.conn.close()

    def init_database(self):
        """Initializes the tables of the database"""

        statement = """
            drop table if exists foodtrucks;
            create table foodtrucks (
                id serial primary key,
                name text not null,
                address text not null,
                fooditems text not null,
                latitude double precision not null,
                longitude double precision not null
            );
        """

        cur = self.conn.cursor()
        cur.execute(statement)
        cur.execute(HAVERSINE_FUNCTION)
        cur.execute(HAVERSINE_FORMULA)
        cur.execute(GREAT_CIRCLE_DISTANCE)
        cur.execute(MILES)
        self.conn.commit()
        cur.close()

    def add_row(self, name, address, fooditems, latitude, longitude):
        """Add a row to the database

        Arguments:
        name -- string - the name field of the new row
        address -- string - the address field of the new row
        fooditems -- string - a ': ' separated list of menu items
        latitude -- float - the latitude of the new row
        longitude -- float - the longitude of the new row
        """

        statement = """
            insert into foodtrucks 
                (name, address, fooditems, latitude, longitude)values 
                (%s, %s, %s, %s, %s)
        """
        cur = self.conn.cursor()
        try:
            cur.execute(
                statement,
                (name, address, fooditems, latitude, longitude)
            )
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            cur.close()
            raise e
        self.conn.commit()
        cur.close()

    def gen_within_distance(self, distance, latitude, longitude):
        """A generator which yields rows within the given distance of the given latitude and longitude

        Arguments:
        distance -- float - the distance for returned rows to be within
        latitude -- float - the latitude to compare against
        longitude -- float - the longitude to compare against
        """

        if distance < 0.0:
            raise ValueError('distance must be a positive number')

        statement = """
            select name, address, fooditems from foodtrucks
            where miles(great_circle_distance(
                radians(latitude),
                radians(longitude),
                radians(%s),
                radians(%s)
            )) <= %s
        """
        cur = self.conn.cursor()
        cur.execute(
            statement,
            (latitude, longitude, distance)
        )
        for row in cur.fetchall():
            foodtruck = {
                key: val for key, val in zip(
                    (d[0] for d in cur.description), 
                    row
                )
            }    
            yield foodtruck
        cur.close()
