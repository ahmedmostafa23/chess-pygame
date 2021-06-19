# This is the main file that contains the gameplay. other files do not contain
# the gameplay, but contain global variables, classes, functions, and assets
from ChessBoard import ChessBoard
from Global import *

# white will always start at the bottom

if __name__ == '__main__':
    cb = ChessBoard(cburl, 768, 0, 0)

    click_xy = None
    click_row_col = None
    ctrl = False
    running = True  # this means that the game as a program is running, not the chess game
    over = False  # this is the chess game

    while True:
        computer_plays = input("'single player' or '2 player'?") # set this to false for 1vs1, but to true to play against the computer
        if computer_plays == "single player":
            computer_plays = True
            break
        elif computer_plays == "2 player":
            computer_plays = False
            break
    turns = ["white", "black"]
    while True:
        turn = input("'black' or 'white' goes first?")  # this will also be the player, and the starting turn
        if turn == "white":
            i = 0
            break
        if turn == "black":
            i = 1
            break

    while running:
        pygame.time.delay(game_loop_ps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not over:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    click_xy = pygame.mouse.get_pos()
                    click_row_col = cb.xy_to_rowcol(click_xy[0], click_xy[1])
                    z = cb.true_move(turn, click_row_col)
                    cb.selected_info()
                    if z:
                        i += 1
                        turn = turns[i % 2]
                        if cb.checkmate(turn):
                            over = True
                            print(f"game over! {turn} loses! {turns[(i+1) % 2]} wins!")
                            if turn == "white":
                                cb.selection = cb.white_king
                            else:
                                cb.selection = cb.black_king
                        elif not cb.checkmate(turn) and computer_plays:
                            cb.random_move(turn)
                            i += 1
                            turn = turns[i % 2]

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    cb.deselect()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        ctrl = True
                    if event.key == pygame.K_z and ctrl:
                        if computer_plays:
                            z = cb.undo()
                            z = cb.undo()
                            if z:
                                i -= 2
                                turn = turns[i % 2]
                        else:
                            z = cb.undo()
                            if z:
                                i -= 1
                                turn = turns[i % 2]

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        ctrl = False

        cb.display_board()

        x = cb.get_selection()
        if x:
            cb.show_moves(*x)
            #cb.show_technically_legal(*x)

        cb.check_threat(turn)
        cb.display_pieces()

        pygame.display.update()

