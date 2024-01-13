import pygame
import utils
from Square import Square
from Point import Point

class Snake:
  IMAGE_body = pygame.transform.scale(pygame.image.load('assets/body.png'), (Square.SQUARE_TOTAL_SIDE_LENGTH,
                                                                                    Square.SQUARE_TOTAL_SIDE_LENGTH))

  IMAGE_head_right = pygame.transform.scale(pygame.image.load('assets/head_right.png'), (Square.SQUARE_TOTAL_SIDE_LENGTH,
                                                                                    Square.SQUARE_TOTAL_SIDE_LENGTH))
  IMAGE_head_left = pygame.transform.scale(pygame.image.load('assets/head_left.png'), (Square.SQUARE_TOTAL_SIDE_LENGTH,
                                                                                    Square.SQUARE_TOTAL_SIDE_LENGTH))
  IMAGE_head_up = pygame.transform.scale(pygame.image.load('assets/head_up.png'), (Square.SQUARE_TOTAL_SIDE_LENGTH,
                                                                                    Square.SQUARE_TOTAL_SIDE_LENGTH))
  IMAGE_head_down = pygame.transform.scale(pygame.image.load('assets/head_down.png'), (Square.SQUARE_TOTAL_SIDE_LENGTH,
                                                                                    Square.SQUARE_TOTAL_SIDE_LENGTH))

  IMAGE_tail_right = pygame.transform.scale(pygame.image.load('assets/tail_right.png'), (Square.SQUARE_TOTAL_SIDE_LENGTH,
                                                                                    Square.SQUARE_TOTAL_SIDE_LENGTH))
  IMAGE_tail_left = pygame.transform.scale(pygame.image.load('assets/tail_left.png'), (Square.SQUARE_TOTAL_SIDE_LENGTH,
                                                                                    Square.SQUARE_TOTAL_SIDE_LENGTH))
  IMAGE_tail_up = pygame.transform.scale(pygame.image.load('assets/tail_up.png'), (Square.SQUARE_TOTAL_SIDE_LENGTH,
                                                                                    Square.SQUARE_TOTAL_SIDE_LENGTH))
  IMAGE_tail_down = pygame.transform.scale(pygame.image.load('assets/tail_down.png'), (Square.SQUARE_TOTAL_SIDE_LENGTH,
                                                                                    Square.SQUARE_TOTAL_SIDE_LENGTH))
  COLOR = '#26de81'

  DIRECTIONS = {
    pygame.K_UP: {'name': 'up', 'movement': Point(0, -1), 'opposite': 'down'},
    pygame.K_RIGHT: {'name': 'right', 'movement': Point(1, 0), 'opposite': 'left'},
    pygame.K_DOWN: {'name': 'down', 'movement': Point(0, 1), 'opposite': 'up'},
    pygame.K_LEFT: {'name': 'left', 'movement': Point(-1, 0), 'opposite': 'right'}
  }

  def __init__(self, position, direction='right'):
    self.squares = [Square("", position)]
    self.direction = self.DIRECTIONS[pygame.K_RIGHT]
    self.is_alive = True

  def move(self, key):
    if (key in self.DIRECTIONS and self.DIRECTIONS[key]['name'] != self.direction['opposite']):
      self.direction = self.DIRECTIONS[key]

    new_square = Square(self.IMAGE_body, self.squares[-1].position + self.direction['movement'])
    if (new_square in self.squares or
    new_square.position.x < 0 or new_square.position.x >= utils.WIDTH or
    new_square.position.y < 0 or new_square.position.y >= utils.HEIGHT):
      self.is_alive = False

    self.squares.append(new_square)

    return new_square.position

  def shrink(self):
    self.squares.pop(0)

  def draw(self, surface):
    image_tail = self.IMAGE_tail_right
    if len(self.squares) > 1:
      if self.squares[0].position + Point(1, 0) == self.squares[1].position:
        image_tail = self.IMAGE_tail_right
      if self.squares[0].position + Point(-1, 0) == self.squares[1].position:
        image_tail = self.IMAGE_tail_left
      if self.squares[0].position + Point(0, 1) == self.squares[1].position:
        image_tail = self.IMAGE_tail_down
      if self.squares[0].position + Point(0, -1) == self.squares[1].position:
        image_tail = self.IMAGE_tail_up
    tail = Square(image_tail, Point(self.squares[0].position.x, self.squares[0].position.y))
    tail.draw_image(surface)
    for square in self.squares[1:-1]:
      square.draw_image(surface)

    image_head = self.IMAGE_head_right
    match self.direction["name"]:
      case "right":
        image_head = self.IMAGE_head_right
      case "left":
        image_head = self.IMAGE_head_left
      case "up":
        image_head = self.IMAGE_head_up
      case "down":
        image_head = self.IMAGE_head_down
    head = Square(image_head, Point(self.squares[-1].position.x, self.squares[-1].position.y))
    head.draw_image(surface)