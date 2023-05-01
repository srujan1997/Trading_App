import os
from flask import Flask
import redis

from ping import ping

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]


def create_app(app_name=PKG_NAME):
    app = Flask(app_name)
    app_config = os.environ.get("CONFIG", "config")
    app.config.from_object(app_config)

    app.debug = app.config["DEBUG"]
    app.env = app.config["ENVIRONMENT"]

    app.redis_connection = redis.StrictRedis(
        host=app.config["REDIS"]["HOST"],
        port=app.config["REDIS"]["PORT"],
        db=app.config["REDIS"]["DB"],
        password=app.config["REDIS"]["PASSWORD"],
        socket_timeout=2,
        socket_connect_timeout=2,
    )

    app.url_map.strict_slashes = False

    BASE_URL_PREFIX = f"/api/order_service_{app.config['SERVICE_ID']}"

    with app.app_context():
        app.register_blueprint(ping, url_prefix=f"{BASE_URL_PREFIX}/ping")

    @app.teardown_request
    def teardown_request(exception):
        #  To snapshot service state and gracefully close the application. Currently, doing nothing.
        pass

    return app