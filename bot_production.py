import asyncio
import logging
import random

import aiohttp

from client import game


class BotProduction:
    def __init__(self, loop):
        self._api_url = "http://localhost:8081"
        self._team_name = "Olivyeshka"
        self._session = aiohttp.ClientSession()
        self._game = game
        self._player = {}
        self._loop = loop

    async def _prepare_player(self):
        async with self._session.post(f"{self._api_url}/game",
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
            data = (await response.json())['data']
            logging.info(f'Player {self._player.get("color")} made move {move}, response data: {data}')

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

            move = random.choice(self._game.get_possible_moves())

            await self._make_move(move)

            # evaluating time and deciding which move to do
            player_num_turn = 1 \
                if current_game_progress['whose_turn'] == 'RED' \
                else 2

            current_game_progress = await self._get_game()

            is_started = current_game_progress.get('is_started')
            is_finished = current_game_progress.get('is_finished')

    def start_test(self):
        asyncio.run_coroutine_threadsafe(self.start(), self._loop)

    async def start(self):
        logging.info('API Tester initialized, test will start in 2 secs')
        await asyncio.sleep(2.0)

        asyncio.ensure_future(self._prepare_player())

        logging.info('Game starter. Player initialized')

        await asyncio.sleep(0.5)

        logging.info(f'Player: {self._player}')

        await asyncio.sleep(0.5)

        await self._play_game()

        logging.info('Game finished')
        last_game_progress = await self._get_game()
        logging.info(str(last_game_progress))

        await self._session.close()
