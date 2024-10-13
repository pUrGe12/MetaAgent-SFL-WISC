
document.addEventListener('DOMContentLoaded', () => {
    const gameBoard = document.getElementById('game-board');
    const size = 4;
    let board = [];

    function initBoard() {
        for (let i = 0; i < size; i++) {
            board[i] = [];
            for (let j = 0; j < size; j++) {
                board[i][j] = 0;
                const tile = document.createElement('div');
                tile.classList.add('tile');
                tile.id = `tile-${i}-${j}`;
                gameBoard.appendChild(tile);
            }
        }
        addRandomTile();
        addRandomTile();
        updateBoard();
    }

    function addRandomTile() {
        let emptyTiles = [];
        for (let i = 0; i < size; i++) {
            for (let j = 0; j < size; j++) {
                if (board[i][j] === 0) {
                    emptyTiles.push({ x: i, y: j });
                }
            }
        }
        if (emptyTiles.length > 0) {
            const { x, y } = emptyTiles[Math.floor(Math.random() * emptyTiles.length)];
            board[x][y] = Math.random() < 0.9 ? 2 : 4;
        }
    }

    function updateBoard() {
        for (let i = 0; i < size; i++) {
            for (let j = 0; j < size; j++) {
                const tile = document.getElementById(`tile-${i}-${j}`);
                tile.textContent = board[i][j] === 0 ? '' : board[i][j];
                tile.style.backgroundColor = getTileColor(board[i][j]);
            }
        }
    }

    function getTileColor(value) {
        switch (value) {
            case 2: return '#eee4da';
            case 4: return '#ede0c8';
            case 8: return '#f2b179';
            case 16: return '#f59563';
            case 32: return '#f67c5f';
            case 64: return '#f65e3b';
            case 128: return '#edcf72';
            case 256: return '#edcc61';
            case 512: return '#edc850';
            case 1024: return '#edc53f';
            case 2048: return '#edc22e';
            default: return '#cdc1b4';
        }
    }

    initBoard();
});
