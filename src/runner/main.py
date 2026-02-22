from apexdevkit.server import UvicornServer
from src.runner.setup import setup, get_service
if __name__ == "__main__":
    UvicornServer.from_env().run(setup(get_service()))