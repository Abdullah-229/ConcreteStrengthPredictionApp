import mysql.connector
from mysql.connector import Error

def create_connection():
    """ create a database connection to the MySQL database
        specified by the host, user, password and database
    """
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='cse3200_concreteStrength'
        )
        print("Successfully connected to the database")
    except Error as e:
        print(f"The error '{e}' occurred")
    return conn

def create_table(conn):
    """ create table in the specified database """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cement FLOAT,
                blast_furnace_slag FLOAT,
                fly_ash FLOAT,
                water FLOAT,
                superplasticizer FLOAT,
                coarse_aggregate FLOAT,
                fine_aggregate FLOAT,
                age INT,
                strength_prediction FLOAT,
                quantile_10 FLOAT,
                quantile_90 FLOAT
            )
        """)
        print("Table 'predictions' created successfully or already exists.")
    except Error as e:
        print(f"The error '{e}' occurred")

def insert_prediction(conn, data):
    """
    Insert a new prediction into the predictions table
    :param conn:
    :param data:
    :return:
    """
    # Convert all numpy types to native Python types
    def to_native(val):
        try:
            import numpy as np
            if isinstance(val, (np.generic,)):
                return val.item()
        except ImportError:
            pass
        return val
    data_native = tuple(to_native(x) for x in data)
    sql = ''' INSERT INTO predictions(cement, blast_furnace_slag, fly_ash, water, superplasticizer, coarse_aggregate, fine_aggregate, age, strength_prediction, quantile_10, quantile_90)
              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, data_native)
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"The error '{e}' occurred")
