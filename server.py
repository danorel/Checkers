import asyncio
import threading


def start_server(loop):
    from backend.server import main

    threading \
        .Thread(target=main, args=(loop,)) \
        .start()


def run_ui():
    from board_drawing import BDManager

    BDManager()


if __name__ == '__main__':
    _loop = asyncio.get_event_loop()
    # Run server before client connectivity setup.
    start_server(_loop)
    # Run user interface for checkers.
    run_ui()
    # Run server forever.
    _loop.run_forever()
