import logging
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from api.chess import Chess, ChessException, GameGenParams
from chess import WHITE

app = FastAPI()
chess = Chess()

logger = logging.getLogger(__name__)


class FairGameModel(BaseModel):
    fen: str
    score: int
    ply: int = 0
    turn: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/v1/game/new")
def read_fair_game(params: Annotated[GameGenParams, Query()]) -> FairGameModel:
    params = params or GameGenParams()
    try:
        game = chess.start_game(params)
    except ChessException:
        msg = "Could not find a fair game"
        logger.error(msg)
        raise HTTPException(status_code=404, detail=msg)
    return FairGameModel(
        fen=game.board.fen(),
        score=game.score,
        ply=game.ply,
        turn="white" if game.board.turn == WHITE else "black",
    )
