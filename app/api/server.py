import threading
from urllib import request

import requests
import argparse

from flask import Flask

from app.api.utils import config_parser


class Server:
    def __init__(self, host, port, db_host, db_port, user, password, db_name, rebuild_db=False):
        self.server = None
        self.host = host
        self.port = port

        self.db_interaction = DbInteraction(
            host=db_host,
            port=db_port,
            user=user,
            password=password,
            db_name=db_name,
            rebuild_db=rebuild_db
        )

        self.app = Flask(__name__)
        self.app.add_url_rule('/shutdown', view_func=self.shutdown)
        self.app.add_url_rule('/', view_func=self.get_home)
        self.app.add_url_rule('/home', view_func=self.get_home)
        self.app.add_url_rule('/add_user_info', view_func=, methods=[POST])

    # запуск сервера
    def run_server(self):
        self.server = threading.Thread(target=self.app.run, kwargs={'host': self.host, 'port': self.port})
        self.server.start()
        return self.server

    def shutdown_server(self):
        request.get(f'http://{self.host}:{self.port}/shutdown')

    # функция выключения сервера
    def shutdown(self):
        terminate_func = request.environ.get('werkzeug.server.shutdown')
        if terminate_func:
            terminate_func()

    def get_home(self):
        return 'Server'

    def add_user_info(self):
        request_body = dict(request.json)
        username = request_body['username']
        password = request_body['password']
        email = request_body['email']


# запуск приложения
if __name__ == "__main__":
    # получение настроек из файла -добавляем аргументы
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, dest='config')

    # сохраняем аргументы
    args = parser.parse_args()

    # считываем конфигурационный файл
    config = config_parser(args.config)

    server_host = config['HOST']
    server_port = 8088

    # создаем сервер
    server = Server(
        port=server_port,
        host=server_host

    )
    server.run_server()