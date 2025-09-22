Welcome to King Jet, the main goals of this chess program is as follows:
- easily experiment with tactics
    - branch off easily and go back to main branch
- work with code/graph theory to create bots
    - upload code as models online and pull moves from models stored in cloud

links:
- https://www.youtube.com/watch?v=geHcAS1fFg8
- https://www.freecodecamp.org/news/code-a-chess-game-with-ai-opponent/
- https://stackoverflow.com/questions/64112652/pygame-sometimes-not-detecting-key-presses

TODO:
- (DONE) get color of chessboard square when arbitrarily picked
- (DONE) optimize get_center_coor function in Piece to be generalized
- (DONE) split program into multiple files
- program legal moves
    - proper piece hints in all situations
        - en peassant
        - capturing pieces
    - (DONE) make pieces move
    - (DONE) multi-touch
- (DONE) legal moves only account for black pieces (white pieces go in other direction)
- proper graphic overlay
    - piece hints should not appear when a piece occupies a square
    - square turns different color when piece can attack another piece
    - pieces should not overlay on top of one another
- (DONE) pieces should be part of a larger 'overlay' class

Credits:
- Chess piece art: JohnPablok's improved Cburnett chess set. https://opengameart.org/content/chess-pieces-and-board-squares
- https://stackoverflow.com/questions/2169478/how-to-make-a-checkerboard-in-numpy

Notes:
- (0, 0) is top left, bottom right goes higher
- every change should update status/logic

- show hint logic
    - when mouse clicked, check if occupied (in board status)
    - list all possible moves
        - no move if piece blocks
        - no move if board ends
        - attacks
        - promotions
    - update respective squares
    - update board status
- need game logic to implement check, en passant -> to implement showing hints
- when piece moves, it might be attacked

- pieces stay consistent throughout game, pieces arent being created every time a player moves
