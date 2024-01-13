import pygame

class Square:
  SQUARE_BORDER_WIDTH = 2
  SQUARE_SIDE_LENGTH = 15
  SQUARE_TOTAL_SIDE_LENGTH = SQUARE_SIDE_LENGTH + SQUARE_BORDER_WIDTH * 2
  # Tổng độ dài của mot cạnh hình vuông
  def __init__(self, image, position):
    self.image = image
    self.position = position

  def __eq__(self, other):
    return self.__class__ == other.__class__ and self.position == other.position

  def draw(self, surface, color):
    #rect (trái sang, tren xuống, rộng, dài)
    pygame.draw.rect(surface, color, (
      self.position.x * self.SQUARE_TOTAL_SIDE_LENGTH + self.SQUARE_BORDER_WIDTH,
      self.position.y * self.SQUARE_TOTAL_SIDE_LENGTH + self.SQUARE_BORDER_WIDTH,
      self.SQUARE_SIDE_LENGTH,
      self.SQUARE_SIDE_LENGTH
    ))

  def draw_no_border(self, surface, color):
    pygame.draw.rect(surface, color, (
      self.position.x * self.SQUARE_TOTAL_SIDE_LENGTH,
      self.position.y * self.SQUARE_TOTAL_SIDE_LENGTH,
      self.SQUARE_TOTAL_SIDE_LENGTH,
      self.SQUARE_TOTAL_SIDE_LENGTH
    ))
  def draw_image(self, surface):
    square_image = self.image
    square = square_image.get_rect()
    square.topleft = \
      (self.position.x * Square.SQUARE_TOTAL_SIDE_LENGTH,
       self.position.y * Square.SQUARE_TOTAL_SIDE_LENGTH)
    surface.blit(square_image, square)