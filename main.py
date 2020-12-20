import asyncio
import sys
import threading

from monkey_patched.game import Game

# Init components
game = Game()


def start_server(loop):
    from backend.server import main

    threading.Thread(target=main, args=(loop,)).start()


def client_test(loop, rand_sleep=False):
    from bot_test import BotTester

    threading.Thread(target=BotTester(loop, rand_sleep=rand_sleep).start_test).start()


def client_production(loop):
    from bot_production import BotProduction

    threading.Thread(target=BotProduction(loop).start_test).start()


def run_ui():
    from board_drawing import BDManager

    BDManager()


if __name__ == '__main__':
    _loop = asyncio.get_event_loop()
    # Run server before client connectivity setup.
    start_server(_loop)
    # Run client if modes: test or production.
    if sys.argv.__len__() > 1:
        if sys.argv[1] == '--production':
            client_production(_loop)
        elif sys.argv[1] == '--test':
            client_test(_loop,
                        rand_sleep=False)
        else:
            raise RuntimeError(text="Unknown game mode."
                                    "Pass --test for test_server."
                                    "Pass --production for start_server.")
    else:
        raise RuntimeError(text="Not defined the game mode in parameters."
                                "Setup --test parameter for test_server."
                                "Setup --production parameter for start_server.")
    run_ui()
    _loop.run_forever()
