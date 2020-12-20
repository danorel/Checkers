import asyncio
import logging
import random
import time

import aiohttp

from client import game

from algorithm.Solver import next_move
from algorithm.Minimax import Minimax
from algorithm.Heuristic import Heuristic


class BotTester:
    def __init__(self, loop, rand_sleep):
        self._api_url = "http://localhost:8081"
        self._team_name = "Olivyeshka"
        self._session = aiohttp.ClientSession()
        self._game = game
        self._player = {}
        self._rand_sleep = rand_sleep
        self._time_to_move = 3.2
        self._loop = loop
        self._player_num = None

    async def _prepare_player(self):
        async with self._session.post(
                f'{self._api_url}/game',
                params={'team_name': self._team_name}
        ) as resp:
            res = (await resp.json())['data']
            self._player = {
                'color': res['color'],
                'token': res['token']
            }

    async def _make_move(self, move):
        json = {'move': move}
        headers = {'Authorization': f'Token {self._player["token"]}'}
        async with self._session.post(
                f'{self._api_url}/move',
                json=json,
                headers=headers
        ) as resp:
            resp = (await resp.json())['data']
            logging.info(f'Player {self._player} made move {move}, response: {resp}')

    async def _get_game(self):
        async with self._session.get(f'{self._api_url}/game') as resp:
            return (await resp.json())['data']

    async def _play_game(self):
        current_game_progress = await self._get_game()

        is_started = current_game_progress['is_started']
        is_finished = current_game_progress['is_finished']

        while is_started and not is_finished:
            if current_game_progress['whose_turn'] != self._player['color']:

                current_game_progress = await self._get_game()

                is_started = current_game_progress['is_started']
                is_finished = current_game_progress['is_finished']

                await asyncio.sleep(0.1)
                continue

            last_move = current_game_progress['last_move']
            logging.debug(f"last_move: {last_move}")

            if last_move and last_move['player'] != self._player['color']:
                for move in last_move['last_moves']:
                    self._game.move(move)

            player_num_turn = 1 \
                if current_game_progress['whose_turn'] == 'RED' \
                else 2

            time_start = time.time()
            # best_move = self._find_best_move()
            best_move = next_move(self._game, 4, player_num_turn, True)
            time_end = time.time()

            logging.debug(f"Finding best move time: {time_end - time_start}")

            if not best_move:
                break

            self._game.move(best_move)
            await self._make_move(best_move)

            # move = random.choice(self._game.get_possible_moves())
            # logging.info(move)

            current_game_progress = await self._get_game()

            is_started = current_game_progress['is_started']
            is_finished = current_game_progress['is_finished']

    def start_test(self):
        asyncio.run_coroutine_threadsafe(self.start(), self._loop)

    async def start(self):
        logging.info('API Tester initialized, test will start in 2 secs')

        await asyncio.ensure_future(self._prepare_player())

        logging.info('Game starter. Player initialized')

        await asyncio.sleep(0.5)

        logging.info(f'Player: {self._player}')

        await asyncio.sleep(0.5)

        await self._play_game()

        logging.info('Game finished')
        last_game_progress = await self._get_game()
        logging.info(str(last_game_progress))

        await self._session.close()

    def _find_best_move(self):
        logging.info(f"Try find best local move with available time: {self._time_to_move}")
        return Minimax() \
            .find_best_move(self._time_to_move, game, Heuristic(1, 1, 1, 1, 0, 0))
