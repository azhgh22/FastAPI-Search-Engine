from apexdevkit.server import UvicornServer
from src.runner.setup import setup, get_service_with_vector_engine, get_service_with_vector_engine_sqlite_db

if __name__ == "__main__":
    UvicornServer.from_env().run(setup(get_service_with_vector_engine_sqlite_db()))