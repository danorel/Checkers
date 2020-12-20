import asyncio
import logging
import random
import time

import aiohttp

from client import game

from algorithm.Solver import next_move


class BotTester:
    def __init__(self, loop, rand_sleep):
        self._api_url = "http://localhost:8081"
        self._team_name = "Olivyeshka"
        self._session = aiohttp.ClientSession()
        self._game = game
        self._loop = loop
        self._player = {}
        self._rand_sleep = rand_sleep
        self._time_to_move = 3.2

    async def _prepare_player(self):
        async with self._session.post(f'{self._api_url}/game',
                                      params={'team_name':
                                              self._team_name}) as resp:
            res = (await resp.json())['data']
            self._player = {
                'color': res.get('color'),
                'token': res.get('token')
            }

    async def _make_move(self, move):
        json = {'move': move}
        headers = {'Authorization': f'Token {self._player.get("token")}'}
        async with self._session.post(f'{self._api_url}/move',
                                      json=json,
                                      headers=headers) as response:
            logging.debug(f"A try to make movement: {await response.json()}")
            data = (await response.json())['data']
            logging.info(
                f'Player {self._player.get("color")} made move {move}, response data: {data}')

    async def _get_game(self):
        async with self._session.get(f'{self._api_url}/game') as response:
            return (await response.json())['data']

    async def _play_game(self):
        current_game_progress = await self._get_game()

        is_started = current_game_progress.get('is_started')
        is_finished = current_game_progress.get('is_finished')

        while is_started and not is_finished:
            if current_game_progress.get('whose_turn') != self._player.get('color'):

                current_game_progress = await self._get_game()

                is_started = current_game_progress.get('is_started')
                is_finished = current_game_progress.get('is_finished')

                await asyncio.sleep(0.1)
                continue

            logging.info(f"Current game progress: {current_game_progress}")

            enemy_move = current_game_progress.get('last_move', None)
            logging.debug(f"Last enemy move: {enemy_move}")

            # If the enemy has worked out any movement
            if (enemy_move is not None) and (enemy_move.get('player') != self._player.get('color')):
                for move in enemy_move.get('last_moves'):
                    logging.debug(f'Applying last enemy move: {move}')
                    self._game.move(move)

            player_num_turn = 1 \
                if current_game_progress.get('whose_turn') == 'RED' \
                else 2

            time_start = time.time()
            best_move = next_move(game=self._game,
                                  depth=4,
                                  maximizing_player=player_num_turn,
                                  test=False)
            logging.debug(f"Best move to do: {best_move}")
            time_end = time.time()

            logging.debug(f"Finding best move time: {time_end - time_start}")

            if not best_move:
                break

            self._game.move(best_move)
            await self._make_move(best_move)

            current_game_progress = await self._get_game()

            is_started = current_game_progress.get('is_started')
            is_finished = current_game_progress.get('is_finished')

    def start_test(self):
        asyncio.run_coroutine_threadsafe(self.start(), self._loop)

    async def start(self):
        logging.info('API Bot Testing initialized. Test will start now')

        await asyncio.ensure_future(self._prepare_player())

        logging.info('Game starter. Player initialized')
        await asyncio.sleep(0.5)

        logging.info(f'Player: {self._player}')
        await asyncio.sleep(0.5)

        await self._play_game()
        logging.info('Game finished successfully')
        
        _game_results = await self._get_game()
        logging.info(str(_game_results))

        await self._session.close()
