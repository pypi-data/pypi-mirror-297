from websocket import create_connection
from chatterbox_bus_client.client import MessageBusClient
from chatterbox_bus_client.message import Message
from chatterbox_bus_client.conf import get_bus_config


def send(message_to_send, data_to_send=None, config=None):
    """Send a single message over the websocket.

    Args:
        message_to_send (str): Message to send
        data_to_send (dict): data structure to go along with the
            message, defaults to empty dict.
        config (dict): websocket configuration
    """
    data_to_send = data_to_send or {}
    config = config or get_bus_config()
    url = MessageBusClient.build_url(config.get("host"),
                                     config.get("port"),
                                     config.get("route"),
                                     config.get("ssl"))

    # Send the provided message/data
    ws = create_connection(url)
    packet = Message(message_to_send, data_to_send).serialize()
    ws.send(packet)
    ws.close()
