import pygame as pg
import sys
import game_objects as go


class Game:
    def __init__(self):
        pg.init()
        self.main_color = go.background
        self.WINDOW_SIZE = 800
        self.TILE_SIZE = 40
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.new_game()
        self.pause = False
        self.end = False
        self.font = pg.font.SysFont("Comic Sans", 40)
        self.winner = ''
        self.losser = ''

    def new_game(self):
        self.snake1 = go.Snake(self, go.snake1, [pg.K_a, pg.K_d, pg.K_w, pg.K_s], 'green', 'images/snake1.png')
        self.snake2 = go.Snake(self, go.snake2, [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN], 'blue', 'images/snake2.png')
        self.food = go.Food(self)
        self.food1 = go.Food(self)
        self.food2 = go.Food(self)
        self.end = False
    def update_game(self):
        pg.display.flip()
        self.clock.tick(60)
        self.snake1.update()
        self.snake2.update()

    def draw_game(self):
        self.screen.fill(self.main_color)
        self.food.draw()
        self.food1.draw()
        self.food2.draw()
        self.snake1.draw()
        self.snake2.draw()

    def draw_start_menu(self):
        pass

    def draw_winner(self, winner):
        self.screen.fill(self.main_color)
        go.draw_text(self, f"The lossers is  {winner}",
                     self.font, go.dark_pink, self.WINDOW_SIZE // 4, self.WINDOW_SIZE // 2)
        go.draw_text(self, f"To play again click SPACE",
                     self.font, go.dark_pink, self.WINDOW_SIZE // 4, self.WINDOW_SIZE // 2 + 50)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            self.snake1.control(event)
            self.snake2.control(event)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.new_game()

    def run(self):
        while True:
            self.check_events()
            self.update_game()
            if self.pause:
                self.draw_start_menu()
            elif self.end:
                self.draw_winner(self.losser)
            else:
                self.draw_game()


if __name__ == '__main__':
    game = Game()
    game.run()

