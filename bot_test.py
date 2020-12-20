import asyncio
import logging
import random
import time

import aiohttp

from client import game

from algorithm.Solver import next_move


class BotTester:
    def __init__(self, loop):
        self._api_url = "http://localhost:8081"
        self._team_name = "Olivyeshka"
        self._session = aiohttp.ClientSession()
        self._game = game
        self._loop = loop
        self._player = {}
        self._last_move = None
        self._time_to_move = 3.2

    async def _prepare_player(self):
        async with self._session.post(f'{self._api_url}/game',
                                      params={'team_name': self._team_name}) as response:
            data = (await response.json())['data']
            self._player = {
                'color': data.get('color'),
                'token': data.get('token')
            }

    async def _make_move(self, move):
        json = {'move': move}
        headers = {'Authorization': f'Token {self._player.get("token")}'}
        async with self._session.post(f'{self._api_url}/move',
                                      json=json,
                                      headers=headers) as response:
            logging.debug(f"A try to make movement: {await response.text()}")
            data = (await response.json())['data']
            logging.debug(
                f'Player {self._player.get("color")} made move: {move}. Response data: {data}')

    async def _get_game(self):
        async with self._session.get(f'{self._api_url}/game') as response:
            logging.debug(f"A try to connect to game: {await response.json()}")
            return (await response.json())['data']

    async def _play_game(self):

        # Read the starter game progress.
        game_progress = await self._get_game()
        logging.info(f"Current game progress: {game_progress}")

        # Get the is_started and is_finished statuses
        # From the game server.
        is_started = game_progress.get('is_started')
        is_finished = game_progress.get('is_finished')

        while is_started and not is_finished:

            # Enemy's turn. Waiting till our turn.
            if game_progress.get('whose_turn') != self._player.get('color'):
                game_progress = await self._get_game()

                is_started = game_progress.get('is_started')
                is_finished = game_progress.get('is_finished')

                await asyncio.sleep(0.15)
                continue

            # storing last moves of the opponent
            last_move = game_progress.get('last_move')
            if last_move and last_move.get('player') != self._player.get('color'):
                for move in last_move.get('last_moves'):
                    self._game.move(move)

            # evaluating time and deciding which move to do
            player_num_turn = 1 \
                if game_progress.get('whose_turn') == 'RED' \
                else 2

            move = next_move(game=self._game,
                             depth=4,
                             maximizing_player=player_num_turn,
                             test=False)

            if not move:
                break

            self._game.move(move)
            await self._make_move(move)

            game_progress = await self._get_game()

            is_started = game_progress.get('is_started')
            is_finished = game_progress.get('is_finished')

    def start_test(self):
        asyncio.run_coroutine_threadsafe(self.start(), self._loop)

    async def start(self):
        try:
            logging.info('API Bot Testing initialized. Test will start now')
            await asyncio.sleep(2.0)

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

        except Exception as exception:
            logging.error(exception)
