import asyncio
import logging
import threading

from monkey_patched.game import Game

# Init components
game = Game()


def start_server(loop):
    from backend.server import main

    threading.Thread(target=main, args=(loop,)).start()


def run_ui():
    from board_drawing import BDManager

    BDManager()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    _loop = asyncio.get_event_loop()
    # Run server before client connectivity setup.
    start_server(_loop)
    # Run user interface for checkers.
    run_ui()
