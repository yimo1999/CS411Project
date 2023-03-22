"""Setup at app startup"""
import os
import sqlalchemy
from flask import Flask
from yaml import load, Loader



def init_connection_engine():
    """ initialize database setup
    Takes in os variables from environment if on GCP
    Reads in local variables that will be ignored in public repository.
    Returns:
        pool -- a connection to GCP MySQL
    """


    # detect env local or gcp

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username='root',
            password='123123',
            database='db',
            host='35.223.202.39'
        )
    )

    return pool


app = Flask(__name__)
db = init_connection_engine()
conn = db.connect()
query_results = conn.execute("Select * from Account;").fetchall()
conn.close()
res = []
for result in query_results:
    item = {
        'id': result[0],
        'task': result[1],
        'status': result[2]
    }

print(res)

# To prevent from using a blueprint, we use a cyclic import
# This also means that we need to place this import here
# pylint: disable=cyclic-import, wrong-import-position

