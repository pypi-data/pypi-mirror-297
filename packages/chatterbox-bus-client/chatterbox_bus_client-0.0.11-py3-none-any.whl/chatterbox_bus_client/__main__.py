from chatterbox_bus_client import client_from_config

if __name__ == "__main__":
    bus = client_from_config()
    bus.run_in_thread()
    bus.on("message", lambda k: print(k))  # print messages
    while True:
        try:
            pass
        except KeyboardInterrupt:
            break
    bus.close()
