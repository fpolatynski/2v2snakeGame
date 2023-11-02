import pygame as pg
import sys
import game_objects as go


class Game:
    def __init__(self):
        self.player1 = None
        pg.init()
        self.main_color = go.background
        self.WINDOW_SIZE = 1200
        self.TILE_SIZE = 30
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        pg.display.set_caption("Pinky Snake")
        self.clock = pg.time.Clock()
        self.pause = True
        self.end = False
        self.font = pg.font.SysFont("Comic Sans", 40)
        self.table = []
        self.player1_img = pg.image.load('images/1player.png').convert_alpha()
        self.player2_img = pg.image.load('images/2player.png').convert_alpha()
        self.player3_img = pg.image.load('images/3player.png').convert_alpha()
        self.player4_img = pg.image.load('images/4player.png').convert_alpha()
        self.exit_img = pg.image.load('images/exit.png').convert_alpha()
        self.player1_button = go.Button(self, 40, 40, self.player1_img, 0.75)
        self.player2_button = go.Button(self, 500, 40, self.player2_img, 0.75)
        self.player3_button = go.Button(self, 40, 500, self.player3_img, 0.75)
        self.player4_button = go.Button(self, 500, 500, self.player4_img, 0.75)
        self.number_of_players = 0
        self.alive = {'red': 1, 'light blue': 0, 'violete': 0, 'dark blue': 0}

    def new_game(self):
        self.snake1 = go.Snake(self, go.snake1, [pg.K_a, pg.K_d, pg.K_w, pg.K_s], 'red', 'images/snake1.png')
        if self.number_of_players > 1:
            self.alive['light blue'] = 1
            self.snake2 = go.Snake(self, go.snake2, [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN], 'light blue', 'images/snake2.png')
        if self.number_of_players > 2:
            self.alive['violete'] = 1
            self.snake3 = go.Snake(self, go.snake3, [pg.K_c, pg.K_b, pg.K_f, pg.K_v], 'violete', 'images/snake3.png')
        if self.number_of_players > 3:
            self.alive['dark blue'] = 1
            self.snake4 = go.Snake(self, go.snake4, [pg.K_j, pg.K_l, pg.K_i, pg.K_k], 'dark blue', 'images/snake4.png')
        self.food = go.Food(self)
        self.food1 = go.Food(self)
        self.food2 = go.Food(self)
        self.end = False

    def update_game(self):
        pg.display.flip()
        self.clock.tick(60)
        if self.alive['red'] == 1:
            self.snake1.update()
        if self.number_of_players > 1 and self.alive["light blue"] == 1:
            self.snake2.update()
        if self.number_of_players > 2 and self.alive["violete"] == 1:
            self.snake3.update()
        if self.number_of_players > 3 and self.alive["dark blue"] == 1:
            self.snake4.update()

    def draw_game(self):
        self.screen.fill(self.main_color)
        self.food.draw()
        self.food1.draw()
        self.food2.draw()
        if self.alive["red"] == 1:
            self.snake1.draw()
        if self.number_of_players > 1 and self.alive["light blue"] == 1:
            self.snake2.draw()
        if self.number_of_players > 2 and self.alive["violete"] == 1:
            self.snake3.draw()
        if self.number_of_players > 3 and self.alive["dark blue"] == 1:
            self.snake4.draw()

    def draw_start_menu(self):
        pg.display.flip()
        self.clock.tick(60)
        self.screen.fill(go.pink)
        if self.player1_button.draw():
            self.number_of_players = 1
            self.new_game()
            self.pause = False
        if self.player2_button.draw():
            self.number_of_players = 2
            self.new_game()
            self.pause = False
        if self.player3_button.draw():
            self.number_of_players = 3
            self.new_game()
            self.pause = False
        if self.player4_button.draw():
            self.number_of_players = 4
            self.new_game()
            self.pause = False

    def check_for_winner(self):
        if not sum(list(self.alive.values())):
            self.end = True

    def draw_winner(self):
        pg.display.flip()
        self.clock.tick(60)
        self.screen.fill(self.main_color)
        go.draw_text(self, f"Wygrywa  {self.table[-1]}",
                     self.font, go.dark_pink, self.WINDOW_SIZE // 4, self.WINDOW_SIZE // 2)
        go.draw_text(self, f"To play again click SPACE",
                     self.font, go.dark_pink, self.WINDOW_SIZE // 4, self.WINDOW_SIZE // 2 + 50)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if self.number_of_players > 0:
                self.snake1.control(event)
            if self.number_of_players > 1:
                self.snake2.control(event)
            if self.number_of_players > 2:
                self.snake3.control(event)
            if self.number_of_players > 3:
                self.snake4.control(event)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.new_game()
                    self.pause = True
                    self.end = False


    def run(self):
        while True:
            self.check_events()
            if self.pause:
                self.draw_start_menu()
            elif self.end:
                self.draw_winner()
                self.check_events()
            else:
                self.update_game()
                self.draw_game()
            self.check_for_winner()


if __name__ == '__main__':
    game = Game()
    game.run()

