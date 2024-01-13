import pygame
import sys
import Square
import Point
import utils

# pygame.init()
#
# # Các biến toàn cục
# screen_width = 800
# screen_height = 600
# square_size = 50
# saved_coordinates = []
#
# # Khởi tạo màn hình
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Draw and Save Squares")
#
# # Hàm vẽ hình vuông
# # def draw_square(x, y):
# #     pygame.draw.rect(screen, (255, 0, 0), (x, y, square_size, square_size))
#
# # Hàm lưu tọa độ vào file text
# def save_coordinates(filename, coordinates):
#     with open(filename, 'w') as file:
#         for coord in coordinates:
#             file.write(f"{coord[0]}, {coord[1]}\n")
#
# # Vòng lặp chính
# running = True
# drawing = False
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 1:  # Nếu là nút trái chuột
#                 x, y = event.pos
#                 saved_coordinates.append((x, y))
#                 drawing = True
#         elif event.type == pygame.MOUSEBUTTONUP:
#             if event.button == 1:
#                 drawing = False
#         elif event.type == pygame.MOUSEMOTION and drawing:
#             x, y = event.pos
#             #draw_square(x - square_size // 2, y - square_size // 2)
#             Square.Square("", Point.Point(x - square_size // 2, y - square_size // 2)).draw(screen, "#ffffff")
#
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_s:  # Nếu nhấn phím 's', lưu tọa độ vào file
#                 save_coordinates("coordinates.txt", saved_coordinates)
#
#     pygame.display.flip()
#
# pygame.quit()
# sys.exit()
pygame.init()
screen = pygame.display.set_mode((utils.SCREEN_WIDTH + 300, utils.SCREEN_HEIGHT))
playing_area = pygame.Surface((utils.SCREEN_WIDTH, utils.SCREEN_HEIGHT))
while True:
    pygame.time.delay(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill("#ffffff")
    playing_area.fill("#cccccc")
    screen.blit(playing_area, (0, 0))
    pygame.display.update()
