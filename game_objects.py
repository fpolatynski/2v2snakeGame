import pygame as pg
from random import randrange


vec2 = pg.math.Vector2
snake1 = (227, 57, 25)
snake2 = (26, 147, 187)
snake3 = (122, 13, 89)
snake4 = (31, 3, 106)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
light_pink = (255, 182, 193)
pink = (255, 105, 180)
dark_pink = (255, 20, 147)
background = (245, 246, 246)


class Snake:
    def __init__(self, game, color, keys, snake_color, image):
        self.color = color
        self.l = keys[0]
        self.r = keys[1]
        self.u = keys[2]
        self.d = keys[3]
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0,
                                  game.TILE_SIZE,
                                  game.TILE_SIZE])
        self.rect.center = self.get_random_position()
        self.direction = vec2(self.size, 0)
        self.step_delay = 100
        self.time = 0
        self.lenght = 1
        self.segments = []
        self.directions = {self.l: 1, self.r: 1, self.u: 1, self.d: 1}
        self.snake_color = snake_color
        self.img = import_image(image, 0.2, (0, 0, 0))
        self.head = self.img

    def end_of_snake(self):
        self.game.alive[self.snake_color] = 0
        self.game.table.append(self.snake_color)
        self.segments = []

    def check_collision(self):
        if self.snake_color != 'red':
            for segment in self.game.snake1.segments:
                if segment.center == self.rect.center:
                    print('a')
                    self.end_of_snake()
        if self.game.number_of_players > 1:
            if self.snake_color != 'light blue':
                for segment in self.game.snake2.segments:
                    if segment.center == self.rect.center:
                        print('b')
                        self.end_of_snake()
        if self.game.number_of_players > 2:
            if self.snake_color != 'violete':
                for segment in self.game.snake3.segments:
                    if segment.center == self.rect.center:
                        print('c')
                        self.end_of_snake()
        if self.game.number_of_players > 3:
            if self.snake_color != 'dark blue':
                for segment in self.game.snake4.segments:
                    if segment.center == self.rect.center:
                        print('d')
                        self.end_of_snake()

    def check_food(self):
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
            self.lenght += 4
        if self.rect.center == self.game.food1.rect.center:
            self.game.food1.rect.center = self.get_random_position()
            self.lenght += 3
        if self.rect.center == self.game.food2.rect.center:
            self.game.food2.rect.center = self.get_random_position()
            self.lenght += 2

    def check_border1(self):
        if self.rect.left < 0 or self.rect.right > self.game.WINDOW_SIZE:
            print('e')
            self.end_of_snake()
        if self.rect.top < 0 or self.rect.bottom > self.game.WINDOW_SIZE:
            print('f')
            self.end_of_snake()

    def check_border(self):
        if self.rect.left < 0:
            self.rect.right = self.game.WINDOW_SIZE
        if self.rect.right > self.game.WINDOW_SIZE:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.bottom = self.game.WINDOW_SIZE
        if self.rect.bottom > self.game.WINDOW_SIZE:
            self.rect.top = 0

    def check_if_collision(self):
        if len(self.segments) > len(set([segment.center for segment in self.segments])):
            print('g')
            print(self.segments)
            #self.end_of_snake()

    def control(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == self.r and self.directions[self.r]:
                self.direction = vec2(self.size, 0)
                self.directions = {self.l: 0, self.r: 0, self.u: 1, self.d: 1}
                self.head = pg.transform.rotate(self.img, 270)

            if event.key == self.u and self.directions[self.u]:
                self.direction = vec2(0, -self.size)
                self.directions = {self.l: 1, self.r: 1, self.u: 0, self.d: 0}
                self.head = self.img
                
            if event.key == self.l and self.directions[self.l]:
                self.direction = vec2(-self.size, 0)
                self.directions = {self.l: 0, self.r: 0, self.u: 1, self.d: 1}
                self.head = pg.transform.rotate(self.img, 90)
                
            if event.key == self.d and self.directions[self.d]:
                self.direction = vec2(0, self.size)
                self.directions = {self.l: 1, self.r: 1, self.u: 0, self.d: 0}
                self.head = pg.transform.rotate(self.img, 180)

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
        self.check_collision()

    def draw(self):
        [pg.draw.rect(self.game.screen, self.color, segment) for segment in self.segments]
        self.game.screen.blit(self.head, (self.rect.left, self.rect.top))


class Food:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.image = import_image('images/fruit1.png', 0.08, (245, 246, 246))
        self.rect = pg.rect.Rect([0, 0,
                                  game.TILE_SIZE - 2,
                                  game.TILE_SIZE - 2])
        self.rect.center = self.get_random_position()

    def get_random_position(self):
        return [randrange(self.size//2,
                          self.game.WINDOW_SIZE -self.size//2,
                          self.size)] * 2

    def draw(self):
        #pg.draw.rect(self.game.screen, (255, 0, 0), self.rect)
        self.game.screen.blit(self.image, (self.rect.left, self.rect.top))


class Button:
    def __init__(self, game, x, y, image, scale):
        self.game = game
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.game.screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


def draw_text(game, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    game.screen.blit(img, (x, y))


def import_image(image, scale, colorkey):
    im = pg.image.load(image)
    im.set_colorkey(colorkey)
    im = pg.transform.scale(im, (int(im.get_width() * scale), int(im.get_height() * scale)))
    return im
