# Jumbo Mana - Technical test

## Test description

A chess game is divided into 3 parts : the opening, the mid game and the final. Openings
are only learned by rote, which limits strategic interest. The purpose of this exercise is to
create a server capable of generating random chess position where black and white are
equals, to initiate the mid game.

**Back-end**  
To create this service, you will develop an API on Python with the FastAPI framework. The
back-end needs to generate only fair chess positions. For that, you will use stockfish to
determinate if the position is equal.

**Front-end**  
A simple front-end will be developing to interact with the back-end and show random fair
chess positions.

## Thought process

First, I looked online to see if someone had already done something similar.
After a quick search, I found this project : [Codepen](https://codepen.io/mherreshoff/full/MWJGwZN) [mherreshoff/fair-chess](https://github.com/mherreshoff/fair-chess/tree/main)
This gave me a starting point to understand how I could use stockfish to evaluate a board position.

Then I read a good portion of the [stockfish documentation](https://official-stockfish.github.io/docs/stockfish-wiki/Home.html).
Some key aspects I learned about stockfish and chess in this documentation:
- There is a standard notation to represent a chess board, called [FEN](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation).
- A way to evaluate a player's advantage in a position is to use the centipawn (`cp`) unit. 100 cp is equivalent to 1 pawn lost.
  When the value is positive, it means that the current player has an advantage, when it's negative the opponent has the advantage.
- A chess move is composed of two `plies`, a `ply` being a move by one player (white or black).
- Stockfish is released as a binary, we can communicate with it using the text-based UCI protocol.
- Stockfish has two commands to generate moves:
  - `eval`: that performs a static evaluation of the current position.
  - `go`: that searches for the best move in the current position.
    This seems to give better results than `eval` but is more computationally expensive.
- The best sequence of moves is called the principal variation (`pv`). Stockfish can return multiple `pv`s, each with a score in centipawns.
- Stockfish supports multithreading, meaning we don't have to handle concurrency ourselves unless we want to spawn multiple stockfish processes.
- Stockfish is designed to give the best moves for a given position. To generate a fair board, we have two possibilities:
  - Ask stockfish for one `pv` each turn, hoping that the advantage will cancel out between both players.
  - Ask stockfish for multiple `pv`s, sort them by their distance from 0, and keep the closest one. This is the approach I chose.

### Basic architecture

![basic sequence diagram](./assets/basic-seq-diagram.png)
The user requests a new game. The webapp queries the API for a fair starting position.

Upon receiving the requests, the API creates a chess board with the standard starting position, then asks
stockfish to propose muliple moves (`pv`) with the `eval` command for this board.

Each `pv` is given a score in centipawns (`cp`) representing the (dis)advantage of the current player.  
We sort the `pvs` by their distance from 0, keep the closest one, and apply the move to the board.

Starting from this new position, the API queries stockfish for new moves, keeping again the move giving the smallest advantage.
This process repeats for a minimum of `min_ply` moves (decided by the user), and until a position giving an advantage under 5 cp is found or `max_ply` has been reached.

### Web UI

![](home.jpg)

The web UI allows to tweak some parameters:
- The max depth of the position evaluation
- The minimum number of ply before considering we're in the mid-game
- The maximum number of ply before giving up on finding a fair board
- The number of pvs to consider each turn

The sidebar also displays some information about the board position:
- The current player
- The relative score in centipawns
- The number of ply it took to reach the fair position

### API

The API has a single endpoint `GET /v1/game/new` that returns a fair board position.
It accepts the following query parameters, matching the UI settings :
- min_ply: `int`. default 16
- max_ply: `int`. default: 26
- max_depth: `int`. default: 20
- max_cp: `int`. default: 5
- max_pv: `int`. default: 5

The response is a JSON object with the following fields:
- fen: str : the FEN representation of the board
- score: int : the relative score in centipawns of the current position
- ply: int = 0 : the number of plies it took to reach this position
- turn: str : the current player


### Improvements

- Generate fair boards ahead of time, and store them in a database. This way, the API can return a fair board instantly,
  without having to wait for stockfish to compute the best move.
- Use an openings database to generate the first few moves of the game, reducing considerably the number of moves to compute.
- Use the `go` command instead of `eval` to get better position evaluation.
- Enable user input on the chessboard, and use stockfish to play against the user.
- Validate the moves played by the user with [chess.js](https://github.com/jhlywa/chess.js)
- Decouple the API from stockfish, use a message queue to communicate with a fleet of stockfish instances.
  Thus we could run stockfish on machines with a higher CPU core count, and deploy less (and smaller) API instances.
- Instead of keeping the worst move each turn, keep the best move hoping that the advantage will cancel out.
- By default the mid-game is considered to be between 16 and 26 plies. Realistically, we should be smarter about this.
  Some say this about the frontier between the opening and the mid-game:
> The opening is the stage of the game in which players develop their pieces, get their king to safety,
> and attempt to control the center. It switches to the middle game when players begin to attack each other, and defend. 

## Technical stack

For this project, I used the following:

**Front-end**
- [Vue 3](https://v3.vuejs.org/) as a JS/TS front-end framework
- [Vite](https://vitejs.dev/) as a JS/TS build tool
- [Tailwind CSS](https://tailwindcss.com/) and [shadcn-vue](https://github.com/unovue/shadcn-vue) because CSS and I don't get along
- [cm-chessboard](https://github.com/shaack/cm-chessboard) an ES6 chessboard library to display the board

**Back-end**
- [FastAPI](https://fastapi.tiangolo.com/) the API framework required
- [pdm](https://pdm.fming.dev/) as a python package management tool
- [chess](https://github.com/niklasf/python-chess) a python library to communicate with stockfish
- [stockfish](https://stockfishchess.org/) as a chess engine

**Notable mentions**
- [neovim](https://neovim.io/) The text editor to rule them all
- [coffee]() to keep me awake

## Getting started

The recommended way to run this project is using `docker` and `docker-compose`.
You will find detailed instructions on how to do so.

Instructions on how to run the project without `docker` are provided in each service's `README.md` ([webapp](./webapp/README.md), [api](./api/README.md)).

### Requirements

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- git

### Building

First, clone this repository:

```bash
git clone https://github.com/joscherrer/jumbo-mana-technical-test.git
cd jumbo-mana-technical-test
```

Docker install instructions can be found here : [](https://docs.docker.com/engine/install/)

To build the `webapp` and `api` images, you can either use `docker-compose` :

```bash
docker-compose build
```

Or build the images separately :

```bash
docker build -t webapp ./webapp/
docker build -t api ./api/
```

### Running

To run the project:

```bash
docker-compose up -d
```

The web application should be available at [http://localhost:8000](http://localhost:8000).
The API docs should be available at [http://localhost:8080/docs](http://localhost:8080/docs).
