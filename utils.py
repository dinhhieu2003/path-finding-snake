from Square import Square
import pygame

SPEED = 30
BACKGROUND_COLOR = '#f6e58d'
HEIGHT = 30
WIDTH = 40
SCREEN_HEIGHT = HEIGHT * Square.SQUARE_TOTAL_SIDE_LENGTH
SCREEN_WIDTH = WIDTH * Square.SQUARE_TOTAL_SIDE_LENGTH
FOOD_IMAGE = pygame.transform.scale(pygame.image.load('assets/food.png'), (Square.SQUARE_TOTAL_SIDE_LENGTH,
                                                                                    Square.SQUARE_TOTAL_SIDE_LENGTH))
SAVE_IMAGE = pygame.transform.scale(pygame.image.load('assets/save.png'), (50, 46))
PAUSE_IMAGE = pygame.transform.scale(pygame.image.load('assets/pause_button.png'), (50, 46))
RESUME_IMAGE = pygame.transform.scale(pygame.image.load('assets/resume_button.png'), (50, 46))
BACK_IMAGE = pygame.transform.scale(pygame.image.load('assets/back_home.png'), (50, 46))
VISUALIZE_IMAGE = pygame.transform.scale(pygame.image.load('assets/visualize_button.png'), (50, 46))
UNVISUALIZE_IMAGE = pygame.transform.scale(pygame.image.load('assets/unvisualize.png'), (50, 46))
CLEAR_IMAGE = pygame.transform.scale(pygame.image.load('assets/clear.png'), (50, 46))

RANK_IMAGE = pygame.transform.scale(pygame.image.load('assets/rank.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
DANGER_IMAGE = pygame.transform.scale(pygame.image.load('assets/danger.png'), (Square.SQUARE_TOTAL_SIDE_LENGTH,
                                                                                    Square.SQUARE_TOTAL_SIDE_LENGTH))
PAUSE_POSITION = SAVE_POSITION = (210, 145)
BACK_POSITION = (210, 195)
VISUALIZE_POSITION = (210, 245)
BACK_POSITION_IN_RANK = (190, 90)
CLEAR_POSITION = (210, 245)