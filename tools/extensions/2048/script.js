
document.addEventListener('DOMContentLoaded', () => {
    const gameBoard = document.getElementById('game-board');
    const scoreDisplay = document.getElementById('score');
    let score = 0;

    function createBoard() {
        for (let i = 0; i < 16; i++) {
            const tile = document.createElement('div');
            tile.classList.add('tile');
            gameBoard.appendChild(tile);
        }
    }

    function generateTile() {
        const tiles = document.querySelectorAll('.tile');
        const emptyTiles = Array.from(tiles).filter(tile => tile.innerHTML === '');
        if (emptyTiles.length === 0) return;
        const randomTile = emptyTiles[Math.floor(Math.random() * emptyTiles.length)];
        randomTile.innerHTML = Math.random() > 0.5 ? 2 : 4;
    }

    function moveTiles() {
        // Implement tile movement logic
    }

    function mergeTiles() {
        // Implement tile merging logic
    }

    function updateScore(points) {
        score += points;
        scoreDisplay.innerHTML = score;
    }

    function control(e) {
        if (e.keyCode === 37) {
            // Left arrow key
            moveTiles();
            mergeTiles();
        } else if (e.keyCode === 38) {
            // Up arrow key
            moveTiles();
            mergeTiles();
        } else if (e.keyCode === 39) {
            // Right arrow key
            moveTiles();
            mergeTiles();
        } else if (e.keyCode === 40) {
            // Down arrow key
            moveTiles();
            mergeTiles();
        }
        generateTile();
    }

    document.addEventListener('keyup', control);
    createBoard();
    generateTile();
    generateTile();
});
