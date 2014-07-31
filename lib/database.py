import inspect
import math
import os
import psycopg2

import haversine

GREAT_CIRCLE_DISTANCE_FUNCTION = """
    create or replace function 
    great_circle_distance(latitude1 real, longitude1 real, latitude2 real, longitude2 real) 
    returns real as $$""" + '\n{0}\n'.format(
        inspect.getsource(haversine)
    ) + """return great_circle_distance(latitude1, longitude1, latitude2, longitude2) $$ 
    language plpythonu"""
MILES_FUNCTION = """
    create or replace function
    miles(kilometers real)
    returns real as $$""" + '\n{0}\n'.format(
        inspect.getsource(haversine)
    ) + """return miles(kilometers) $$ 
    language plpythonu"""
RADIANS_FUNCTION = """
    create or replace function
    radians(degrees real)
    returns real as $$
        import math
        return math.radians(degrees)
    $$ language plpythonu"""

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
                latitude real not null,
                longitude real not null
            );
        """

        cur = self.conn.cursor()
        cur.execute(statement)
        cur.execute(GREAT_CIRCLE_DISTANCE_FUNCTION)
        cur.execute(MILES_FUNCTION)
        cur.execute(RADIANS_FUNCTION)

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
                radians(%s)::real,
                radians(%s)::real
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
