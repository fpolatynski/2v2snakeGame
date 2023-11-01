import pygame as pg
import sys
import game_objects as go


class Game:
    def __init__(self):
        pg.init()
        self.WINDOW_SIZE = 800
        self.TILE_SIZE = 10
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.new_game()

    def draw_grid(self):
        [pg.draw.line(self.screen, (255, 182, 193), (x, 0), (x, self.WINDOW_SIZE)) for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]
        [pg.draw.line(self.screen, (255,192,203), (0, y), (self.WINDOW_SIZE, y)) for y in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]

    def new_game(self):
        self.snake1 = go.Snake(self, (0, 0, 255), [pg.K_a, pg.K_d, pg.K_w, pg.K_s], 1)
        self.snake2 = go.Snake(self, (255,255,0), [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN], 2)
        self.food = go.Food(self)

    def update(self):
        pg.display.flip()
        self.clock.tick(60)
        self.snake1.update()
        self.snake2.update()

    def draw(self):
        self.screen.fill((255, 192, 203))
        #self.draw_grid()
        self.food.draw()
        self.snake1.draw()
        self.snake2.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            self.snake1.control(event)
            self.snake2.control(event)


    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()

