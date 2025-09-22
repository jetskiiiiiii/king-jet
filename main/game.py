import pygame

from resources.ui import *
from pieces import *
from board import *

pygame.init()
screen = pygame.display.set_mode((13*tile_size, 8*tile_size))
clock = pygame.time.Clock()
running = True

dt = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

chessboard_status = BoardStatus()
chessboard_logic = BoardLogic()
chessboard = Board(screen, chessboard_status, chessboard_logic) 

## Main pygame loop
while running:
    event_list = pygame.event.get()
    screen.fill(background)

    ## Render chess pieces
    chessboard.draw_pieces()
    chessboard.fill_rest_of_board()

    for event in event_list:
        dirty_rects = []
        if event.type == pygame.QUIT:
            running = False
        ## get_pressed returns either 3 or 5 buttons
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            chessboard_logic.last_clicked_square = chessboard_logic.clicked_square
            chessboard_logic.clicked_square = (mouse_pos[0] // tile_size, mouse_pos[1] // tile_size) # Tuple of position of square (unscaled)

            clicked_square, last_clicked_square = chessboard_logic.clicked_square, chessboard_logic.last_clicked_square
            piece_of_clicked_square = chessboard_status.status[clicked_square]
            is_correct_side_clicked = True if (piece_of_clicked_square.occupied) and (piece_of_clicked_square.occupied_by.side == chessboard_logic.turn) else False

            # Toggle hint on
            if chessboard.is_click_inside_board(clicked_square):
                # If piece is already showing hints, clicking it again will make hints disappear
                if chessboard_logic.toggle_show_hints:
                    # Toggle hints might be true when player clicks on opposite side
                    if not is_correct_side_clicked:
                        chessboard_logic.toggle_show_hints = False
                    # If player clicks on same piece while hints are showing, hints will disappear
                    if clicked_square == last_clicked_square:
                        chessboard_logic.toggle_show_hints = False
                        break
                    # If hints are shown and player clicks on a hint, move piece
                    elif clicked_square in chessboard_logic.last_hints_shown:
                        chessboard_logic.toggle_show_hints = False
                        chessboard_logic.toggle_move_piece = True
                        break
                # If piece is clicked and square is occupied, show hints
                elif chessboard_status.status[clicked_square].occupied == True and is_correct_side_clicked:
                    chessboard_logic.toggle_show_hints = True

    if chessboard_logic.toggle_show_hints:
        chessboard.draw_piece_hints()

    if chessboard_logic.toggle_move_piece:
        chessboard.move_piece()
        chessboard_logic.toggle_move_piece = False
        chessboard_logic.turn = "dark" if chessboard_logic.turn == "light" else "light"

    pygame.display.update()
    clock.tick(60)

pygame.quit()
