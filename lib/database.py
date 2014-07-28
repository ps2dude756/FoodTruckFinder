import sqlite3

class DataBase:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.conn.row_factory = sqlite3.Row

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
            where (longitude - ?)*(longitude - ?) + 
            (latitude - ?)*(latitude - ?) <= ?
        """
        cur = self.conn.cursor().execute(
            statement,
            (longitude, longitude, latitude, latitude, distance*distance)
        )
        for row in cur.fetchall():
            foodtruck = {key: val for key, val in zip(row.keys(), row)}    
            yield foodtruck
        cur.close()
