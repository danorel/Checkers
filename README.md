# Chekers-Olivyeshka
AI program meant for checkers contest as an exam for Fundamentals of AI course at NaUKMA

This is a client-server application, that is why you need to run them separately in *different terminals*:

Command to run the server: ```python3 server.py```
Command to run the client: ```python3 client.py --production```<br/>

## What were the responsibilities:
1. Creating a board game_drawing.py, connecting to the bot_production.py server, testing bot_test.py - Perch O.
2. The first version of the MinMax algorithm with alpha-beta prunning Solver.py, Heuristic.py, testing, client.py - Orel D.
3. Algorithm modification, testing the coefficients of heuristics - Orel D., Perch O.

## How to run server
1. Install `python 3` and `pip` from https://www.python.org/downloads/.
2. (Optional) Use [`virtualenv`](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for python in order to install modules in project directory only and not to collect trash in your OS.
3. In project folder run `pip install -r requirements.txt`
4. Run such commands in **separate terminals** to see the game in action:<br/>
    4.1. ```python3 server.py``` - to start the checkers' back-end.<br/>
    4.2. ```python3 client.py --prooduction``` - to open the checkers' client **player 1** connection.<br/>
    4.3. Another ```python3 client.py --prooduction``` - to open the checkers' client **player 2** connection.<br/>
> If you have both python 2 and python 3 in your OS, you may want to use `python3` for commands stated above.

> **Note:** Default server host/port is `127.0.0.1:8081`. If you want to run server on non-default host/port, you may change any of these values at `src/server/config/checkers.yaml`. 
