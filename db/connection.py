import psycopg2
from psycopg2 import pool

class Database:
    _connection_pool = None

    @staticmethod
    def initialize(minconn=1, maxconn=10, **db_params):
        if not Database._connection_pool:
            Database._connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn, maxconn, **db_params
            )

    @staticmethod
    def get_connection():
        if Database._connection_pool is None:
            raise Exception("Database connection pool is not initialized.")
        return Database._connection_pool.getconn()

    @staticmethod
    def release_connection(connection):
        if Database._connection_pool:
            Database._connection_pool.putconn(connection)

    @staticmethod
    def close_all_connections():
        if Database._connection_pool:
            Database._connection_pool.closeall()


# Example usage for initialization
db_params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "3835",
    "port": 5432,  # Default PostgreSQL port
}

# Initialize the connection pool
Database.initialize(**db_params)
