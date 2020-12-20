import asyncio
import sys
import threading

from monkey_patched.game import Game

# Init components
game = Game()


def start_server(loop):
    from backend.server import main

    threading.Thread(target=main, args=(loop,)).start()


def test_server(loop, rand_sleep=False):
    from api_tester import ApiTester

    threading.Thread(target=ApiTester(loop, rand_sleep=rand_sleep).start_test).start()


def run_ui():
    from board_drawing import BDManager

    BDManager()


if __name__ == '__main__':
    _loop = asyncio.get_event_loop()
    if sys.argv.__len__() > 1:
        if sys.argv[1] == '--production':
            start_server(_loop)
        elif sys.argv[1] == '--test':
            test_server(_loop,
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
