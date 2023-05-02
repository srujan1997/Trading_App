import os
import socket
import requests

from cache import set_in_redis


port_map = {"1": "6298",
            "2": "7298",
            "3": "8298",
            "default": "6298"
            }


def get_leader_id():
    host_ip = os.environ.get("HOST_IP", "localhost")
    leader = -1
    for i in range(1, 4):
        hostname = f"{os.environ.get('ORDER_SERVICE', host_ip)}_{str(i)}"
        try:
            ip = socket.gethostbyname(hostname)
        except Exception:
            continue
        url = f"http://{ip}:{port_map.get(str(i))}/api/order_service/ping"
        response = requests.get(url)
        if response.status_code == 200 and i > leader:
            leader = i

    notify_leader(leader)
    set_in_redis("leader", leader)
    return str(leader)


def notify_leader(leader):
    for i in range(1, 4):
        hostname = f"order_service_{i}"
        try:
            ip = socket.gethostbyname(hostname)
        except Exception:
            continue
        url = f"http://{ip}:{port_map.get(str(i))}/api/order_service/sync/notify/leader"
        body = {"leader_id": leader}
        response = requests.put(url, json=body)

    return True
