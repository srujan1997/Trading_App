#!/usr/bin/env python3

"""
This module creates a flask instance and ties it up with blueprints
"""

from app_factory import create_app

app = create_app(app_name="order_service")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=app.config['APP_PORT'])