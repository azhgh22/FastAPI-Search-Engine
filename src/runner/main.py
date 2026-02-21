from apexdevkit.server import UvicornServer
from src.runner.setup import setup, get_service_with_in_mem_engine

if __name__ == "__main__":
    UvicornServer.from_env().run(setup(get_service_with_in_mem_engine()))