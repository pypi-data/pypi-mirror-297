import json
import re
from mycroft_bus_client import Message as _Message
from chatterbox_bus_client.encryption import Encryption


class Message(_Message):
    def __init__(self, msg_type, data=None, context=None):
        data = data or {}
        context = context or {}
        super(Message, self).__init__(msg_type=msg_type,
                                      data=data, context=context)
        self.type = self.msg_type  # TODO backwards compatibility, deprecate

    def as_dict(self):
        return {"type": self.msg_type,
                "data": self.data,
                "context": self.context}

    def as_json(self):
        return json.dumps(self.as_dict())

    @staticmethod
    def _get_crypto():
        enc = Encryption()
        if enc.encryption_key:
            return enc
        return None

    @staticmethod
    def from_json(json_string):
        obj = json.loads(json_string)
        return Message(obj.get('type') or '',
                       obj.get('data') or {},
                       obj.get('context') or {})

    @staticmethod
    def from_dict(obj):
        return Message(obj.get('type') or '',
                       obj.get('data') or {},
                       obj.get('context') or {})

    def serialize(self):
        """This returns a string of the message info.

        This makes it easy to send over a websocket. This uses
        json dumps to generate the string with type, data and context

        Returns:
            str: a json string representation of the message.
        """
        payload = json.dumps({
            'type': self.msg_type,
            'data': self.data or {},
            'context': self.context or {}
        })
        encryption = self._get_crypto()
        if encryption:
            payload = encryption.encrypt_as_dict(payload)
            payload = json.dumps(payload)
        return payload

    @staticmethod
    def deserialize(value):
        """This takes a string and constructs a message object.

        This makes it easy to take strings from the websocket and create
        a message object.  This uses json loads to get the info and generate
        the message object.

        Args:
            value(str): This is the json string received from the websocket

        Returns:
            Message: message object constructed from the json string passed
            int the function.
            value(str): This is the string received from the websocket
        """
        payload = json.loads(value)
        encryption = Message._get_crypto()
        if encryption and 'ciphertext' in payload:
            decrypted = encryption.decrypt_from_dict(payload)
            return Message.from_dict(decrypted)
        return Message.from_dict(payload)

    def utterance_remainder(self):
        """
        For intents get the portion not consumed by Adapt.

        For example: if they say 'Turn on the family room light' and there are
        entity matches for "turn on" and "light", then it will leave behind
        " the family room " which is then normalized to "family room".

        Returns:
            str: Leftover words or None if not an utterance.
        """
        # chatterbox style
        if "utterance_remainder" in self.data:
            return self.data["utterance_remainder"]

        # mycroft style (backwards compat) TODO remove
        utt = self.data.get("utterance", "").lower()
        if utt and "__tags__" in self.data:
            # adapt
            for token in self.data["__tags__"]:
                # Substitute only whole words matching the token
                utt = re.sub(r'\b' + token.get("key", "") + r"\b", "", utt)
            return utt.strip()
        return ""

