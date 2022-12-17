import numpy as np
import pygame
import sys
import math
import random

class DropFour:

    def __init__(self, player1_is_human=True, player2_is_human=True, row_count=6, column_count=7, board_color=(0,191,255), background_color=(0, 0, 0), player1_color=(220,20,60), player2_color=(255,255,102)):

        # initalize pygame
        pygame.init()

        # define starting variables
        self.row_count = row_count
        self.column_count = column_count
        self.board_color = board_color
        self.background_color = background_color
        self.player1_color = player1_color
        self.player1_is_human = player1_is_human
        self.player2_color = player2_color
        self.player2_is_human = player2_is_human
        self.game_over = False
        self.player_turn = 1

        self.font = pygame.font.SysFont("monospace", 75)

        # define width and height of board
        self.SQUARESIZE = 100
        self.RADIUS = int(self.SQUARESIZE / 2 - 5)
        self.width = column_count * self.SQUARESIZE
        self.height = (row_count + 1) * self.SQUARESIZE
        size = (self.width, self.height)
        self.screen = pygame.display.set_mode(size)

        # generate and draw board
        self.board = self.create_board()
        self.draw_board()


    def play(self):

        while not self.game_over:
            self.turn_loop()
        pygame.time.wait(1000)

    def turn_loop(self):

        player_color = self.get_color()

        if self.player_turn == 1 and not self.player1_is_human:
            self.take_turn(random.randint(0, self.column_count - 1))
        if self.player_turn == 2 and not self.player2_is_human:
            self.take_turn(random.randint(0, self.column_count - 1))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(self.screen, self.background_color, (0, 0, self.width, self.SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(self.screen, player_color, (posx, int(self.SQUARESIZE / 2)), self.RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(math.floor(posx / self.SQUARESIZE))
                self.take_turn(col)

    def take_turn(self, col):
        pygame.draw.rect(self.screen, self.background_color, (0, 0, self.width, self.SQUARESIZE))

        if self.is_valid_location(col):
            self.drop_piece(col, self.player_turn)

            if self.winning_move(self.player_turn):
                label = self.font.render(f"Player {self.player_turn} wins!!", 1, self.get_color())
                self.screen.blit(label, (40, 10))
                self.game_over = True

        self.draw_board()

        self.player_turn = 1 if self.player_turn == 2 else 2

    def get_color(self):
        if self.player_turn == 1:
            return self.player1_color
        else:
            return self.player2_color

    def create_board(self):
        board = np.zeros((self.row_count, self.column_count))
        return board


    def drop_piece(self, col, piece):
        row = self.get_next_open_row(col)
        self.board[row][col] = piece


    def is_valid_location(self, col):
        return self.board[self.row_count - 1][col] == 0


    def get_next_open_row(self, col):
        for r in range(self.row_count):
                if self.board[r][col] == 0:
                    return r


    def print_board(self):
        print(np.flip(self.board, 0))


    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self.column_count - 3):
            for r in range(self.row_count):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece and self.board[r][
                    c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.column_count):
            for r in range(self.row_count - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece and self.board[r + 3][
                    c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self.column_count - 3):
            for r in range(self.row_count - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][c + 2] == piece and self.board[r + 3][
                    c + 3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.column_count - 3):
            for r in range(3, self.row_count):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][c + 2] == piece and self.board[r - 3][
                    c + 3] == piece:
                    return True


    def draw_board(self):
        for c in range(self.column_count):
            for r in range(self.row_count):
                pygame.draw.rect(self.screen, self.board_color, (c * self.SQUARESIZE, r * self.SQUARESIZE + self.SQUARESIZE,
                                                     self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, self.background_color, (
                    int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int(r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE / 2)),
                                   self.RADIUS)

            for r in range(self.row_count):

                if not self.board[r][c] == 0:
                    if self.board[r][c] == 1:
                        color = self.player1_color
                    if self.board[r][c] == 2:
                        color = self.player2_color
                    pygame.draw.circle(self.screen, color, (
                        int(c * self.SQUARESIZE + self.SQUARESIZE / 2), self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)),
                                       self.RADIUS)
        pygame.display.update()

if __name__ == "__main__":
    game = DropFour(False, False)
    game.play()