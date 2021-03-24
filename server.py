import asyncio
import logging
import threading

from src.client.game import Game

# Init components
game = Game()


def start_server(loop):
    from src.server.rules.server import main

    threading.Thread(target=main, args=(loop,)).start()


def run_ui():
    from src.client.board import BoardDisplay

    BoardDisplay()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    _loop = asyncio.get_event_loop()
    # Run server before client connectivity setup.
    start_server(_loop)
    # Run user interface for checkers.
    run_ui()
