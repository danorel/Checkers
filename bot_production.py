import asyncio
import logging
import random

import aiohttp

from main import game


class BotProduction:
    def __init__(self, loop):
        self._api_url = "http://localhost:8081"
        self._team_name = "Olivyeshka"
        self._session = aiohttp.ClientSession()
        self._game = game
        self._player = {}
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

    async def _make_move(self, player, move):
        json = {'move': move}
        headers = {'Authorization': f'Token {self._player[player]["token"]}'}
        async with self._session.post(
                f'{self._api_url}/move',
                json=json,
                headers=headers
        ) as resp:
            resp = (await resp.json())['data']
            logging.info(f'Player {player} made move {move}, response: {resp}')

    async def _get_game(self):
        async with self._session.get(f'{self._api_url}/game') as resp:
            return (await resp.json())['data']

    async def _play_game(self):
        current_game_progress = await self._get_game()
        print(current_game_progress)
        is_finished = current_game_progress['is_finished']
        is_started = current_game_progress['is_started']

        while is_started and not is_finished:
            player_num_turn = 1 if current_game_progress['whose_turn'] == 'RED' else 2
            assert self._game.whose_turn() == player_num_turn

            move = random.choice(self._game.get_possible_moves())

            await self._make_move(player_num_turn, move)

            if self._rand_sleep:
                await asyncio.sleep(random.uniform(1.0, 3.5))
            else:
                await asyncio.sleep(0.2)

            current_game_progress = await self._get_game()
            is_finished = current_game_progress['is_finished']
            is_started = current_game_progress['is_started']

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
