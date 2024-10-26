import logging

from dataclasses import dataclass
import os
from chess.engine import Cp, InfoDict, PovScore, SimpleEngine, Limit
from chess import WHITE, Board
from pydantic import BaseModel, Field


AVAILABLE_CPU_COUNT = len(os.sched_getaffinity(0))
logger = logging.getLogger(__name__)


# Used to sort the PVs by unsigned score
def pv_sort_predicate(pv: InfoDict) -> int:
    if "score" not in pv:
        return 1000
    return abs(pv["score"].white().score() or 1000)


class GameGenParams(BaseModel):
    min_ply: int = Field(default=16, gt=0, le=20)
    max_ply: int = Field(default=26, gt=20, le=50)
    max_depth: int = Field(default=10, gt=0, le=30)
    max_cp: int = Field(default=5, gt=0, le=10)
    max_pv: int = Field(default=5, gt=0, le=10)


@dataclass
class FairGame:
    board: Board
    initial_pov_score: PovScore
    ply: int = 0

    @property
    def uint_score(self) -> int:
        """
        Returns the unsigned score value for the current color.
        """
        return abs(self.score)

    @property
    def score(self) -> int:
        """
        Returns the relative signed score value for the current color.
        """
        return self.initial_pov_score.pov(self.board.turn).score() or 1000


class ChessException(Exception):
    pass


class Chess:
    _engine: SimpleEngine

    def __init__(self):
        self._engine = SimpleEngine.popen_uci("stockfish", debug=True)
        self._engine.configure({"Threads": AVAILABLE_CPU_COUNT})

    def start_game(self, params: GameGenParams | None = None) -> FairGame:
        """
        Starts a new game, returning the fairest one.
        """
        params = params or GameGenParams()

        b = Board()
        score: PovScore = PovScore(Cp(1000), b.turn)

        fairest = FairGame(b.copy(), score, 0)

        for ply in range(params.max_ply):
            logger.debug(
                f"Running eval at ply {ply}, turn {"white" if b.turn == WHITE else "black"}"
            )
            pvs = self._engine.analyse(
                b, limit=Limit(depth=params.max_depth), multipv=params.max_pv
            )

            pvs.sort(key=pv_sort_predicate)

            if "pv" not in pvs[0]:
                msg = f"Stockfish eval did not return any pv at ply {ply}"
                raise ChessException(msg)

            if "score" not in pvs[0]:
                msg = f"Stockfish eval did not return a score at ply {ply}"
                raise ChessException(msg)

            b.push(pvs[0]["pv"][0])
            score = pvs[0]["score"]

            if ply <= params.min_ply:
                logger.debug(
                    f"Skipping candidate: ply {ply} < min_ply {params.min_ply}"
                )
                continue

            candidate = FairGame(Board(b.fen()), score, ply)
            logger.debug(f"candidate: {candidate.uint_score} - {candidate.ply}")

            if candidate.uint_score < params.max_cp:
                fairest = candidate
                break

        if fairest.uint_score > params.max_cp:
            raise ChessException("No fair game found")

        return fairest
