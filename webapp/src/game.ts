import { Chessboard } from "cm-chessboard/src/Chessboard.js";

class BoardInfo {
    fen: string;
    score: number;
    turn: string;

    constructor(fen: string, score: number, turn: string) {
        this.fen = fen;
        this.score = score;
        this.turn = turn;
    }
}

class Game {
    board: Chessboard;
    tagId: string;
    boardInfo: BoardInfo;

    constructor(tagId: string, boardInfo: BoardInfo) {
        this.tagId = tagId;
        this.boardInfo = boardInfo;
        console.log("Game created");
    }

    start() {
        this.board = new Chessboard(document.getElementById(this.tagId), {
            position: this.boardInfo.fen,
            assetsUrl: "/chessboard/"
        });
    }
}

export default Game;
