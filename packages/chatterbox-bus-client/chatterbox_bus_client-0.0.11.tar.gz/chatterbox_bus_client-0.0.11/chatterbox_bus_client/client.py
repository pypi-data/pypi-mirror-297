from mycroft_bus_client import MessageBusClient as MycroftBusClient
from mycroft_bus_client.client import MessageWaiter
from chatterbox_bus_client.message import Message


class MessageBusClient(MycroftBusClient):
    def on_message(self, message):
        # override to use the chatterbox Message object that handles crypto!
        parsed_message = Message.deserialize(message)
        self.emitter.emit('message', message)
        self.emitter.emit(parsed_message.msg_type, parsed_message)
