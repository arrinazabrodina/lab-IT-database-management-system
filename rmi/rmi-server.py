import Pyro5.api
import sys
import os

uri_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "uri.txt")

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rmi'))
from RmiDatabaseManager import RmiDatabaseManager


def start_server():
    with Pyro5.api.Daemon() as daemon:
        uri = daemon.register(RmiDatabaseManager)

        with open(uri_file, "w") as file:
            file.write(str(uri))

        print(f"Сервер запущений з URI: {uri}")
        print(f"URI збережено у файлі: {uri_file}")

        daemon.requestLoop()


if __name__ == "__main__":
    start_server()