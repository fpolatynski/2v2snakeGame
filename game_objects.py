import pygame as pg
from random import randrange

vec2 = pg.math.Vector2


class Snake:
    def __init__(self, game, color, keys):
        self.color = color
        self.l = keys[0]
        self.r = keys[1]
        self.u = keys[2]
        self.d = keys[3]
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0,
                                  game.TILE_SIZE - 2,
                                  game.TILE_SIZE - 2])
        self.rect.center = self.get_random_position()
        self.direction = vec2(0, 0)
        self.step_delay = 100
        self.time = 0
        self.lenght = 1
        self.segments = []
        self.directions = {self.l: 1, self.r: 1, self.u: 1, self.d: 1}

    def check_food(self):
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
            self.lenght += 5

    def check_border(self):
        if self.rect.left < 0 or self.rect.right > self.game.WINDOW_SIZE:
            self.game.new_game()
        if self.rect.top < 0 or self.rect.bottom > self.game.WINDOW_SIZE:
            self.game.new_game()

    def check_if_collision(self):
        if len(self.segments) > len(set([segment.center for segment in self.segments])):
            self.game.new_game()

    def control(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == self.r and self.directions[self.r]:
                self.direction = vec2(self.size, 0)
                self.directions = {self.l: 0, self.r: 1, self.u: 1, self.d: 1}
            if event.key == self.u and self.directions[self.u]:
                self.direction = vec2(0, -self.size)
                self.directions = {self.l: 1, self.r: 1, self.u: 1, self.d: 0}
                
            if event.key == self.l and self.directions[self.l]:
                self.direction = vec2(-self.size, 0)
                self.directions = {self.l: 1, self.r: 0, self.u: 1, self.d: 1}
                
            if event.key == self.d and self.directions[self.d]:
                self.direction = vec2(0, self.size)
                self.directions = {self.l: 1, self.r: 1, self.u: 0, self.d: 1}

    def control2(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT and self.directions[pg.K_d]:
                self.direction = vec2(self.size, 0)
                self.directions = {pg.K_d: 1, pg.K_w: 1, pg.K_a: 0, pg.K_s: 1}

            if event.key == pg.K_UP and self.directions[pg.K_w]:
                self.direction = vec2(0, -self.size)
                self.directions = {pg.K_d: 1, pg.K_w: 1, pg.K_a: 1, pg.K_s: 0}

            if event.key == pg.K_LEFT and self.directions[pg.K_a]:
                self.direction = vec2(-self.size, 0)
                self.directions = {pg.K_d: 0, pg.K_w: 1, pg.K_a: 1, pg.K_s: 1}

            if event.key == pg.K_DOWN and self.directions[pg.K_s]:
                self.direction = vec2(0, self.size)
                self.directions = {pg.K_d: 1, pg.K_w: 0, pg.K_a: 1, pg.K_s: 1}

    def delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time > self.step_delay:
            self.time = time_now
            return True
        return False

    def get_random_position(self):
        return [randrange(self.size//2,
                          self.game.WINDOW_SIZE -self.size//2,
                          self.size)] * 2
    
    def move(self):
        if self.delta_time():
            self.rect.move_ip(self.direction)
            self.segments.append(self.rect.copy())
            self.segments = self.segments[-self.lenght:]

    def update(self):
        self.move()
        self.check_food()
        self.check_border()
        self.check_if_collision()

    def draw(self):
        [pg.draw.rect(self.game.screen, self.color, segment) for segment in self.segments]
        pg.draw.rect(self.game.screen, self.color, self.rect)


class Food:
    def __init__(self, game):
            self.game = game
            self.size = game.TILE_SIZE
            self.rect = pg.rect.Rect([0, 0,
                                      game.TILE_SIZE - 2,
                                      game.TILE_SIZE - 2])
            self.rect.center = self.get_random_position()

    def get_random_position(self):
        return [randrange(self.size//2,
                          self.game.WINDOW_SIZE -self.size//2,
                          self.size)] * 2

    def draw(self):
        pg.draw.rect(self.game.screen, (255, 0, 0), self.rect)
