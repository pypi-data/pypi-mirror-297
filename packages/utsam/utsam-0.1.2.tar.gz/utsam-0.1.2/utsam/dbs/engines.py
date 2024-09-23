from sqlalchemy import create_engine

def create_pg_engine(
    database_type: str,
    username: str,
    password: str,
    host: str,
    port: str,
    database_name: str,
    echo = False
    ):
    # Create a connection string
    connection_string = f'{database_type}://{username}:{password}@{host}:{port}/{database_name}'

    # Create a database engine
    return create_engine(connection_string, pool_size=10, max_overflow=0, echo=echo)
