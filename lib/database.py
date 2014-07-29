import math
import sqlite3

from haversine import great_circle_distance, miles

class DataBase:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.conn.row_factory = sqlite3.Row
        self.conn.create_function(
            'great_circle_distance', 4, great_circle_distance
        )
        self.conn.create_function('radians', 1, math.radians)
        self.conn.create_function('miles', 1, miles)

    def __del__(self):
        self.conn.close()

    def init_database(self):
        statement = """
            drop table if exists foodtrucks;
            create table foodtrucks (
                id integer primary key autoincrement,
                name text not null,
                address text not null,
                fooditems text not null,
                latitude real not null,
                longitude real not null
            );
        """
        cur = self.conn.cursor()
        cur.executescript(statement)
        self.conn.commit()
        cur.close()

    def add_row(self, name, address, fooditems, longitude, latitude):
        statement = """
            insert into foodtrucks 
                (name, address, fooditems, longitude, latitude)
                values (?, ?, ?, ?, ?)
        """
        cur = self.conn.cursor()
        cur.execute(
            statement,
            (name, address, fooditems, latitude, longitude)
        )
        self.conn.commit()
        cur.close()

    def gen_within_distance(self, distance, longitude, latitude):
        if distance < 0.0:
            raise ValueError('distance must be a positive number')

        statement = """
            select name, address, fooditems from foodtrucks
            where miles(great_circle_distance(
                radians(longitude),
                radians(latitude),
                radians(?),
                radians(?)
            )) <= ?
        """
        cur = self.conn.cursor().execute(
            statement,
            (longitude, latitude, distance)
        )
        for row in cur.fetchall():
            foodtruck = {key: val for key, val in zip(row.keys(), row)}    
            yield foodtruck
        cur.close()
