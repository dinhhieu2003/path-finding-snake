import pygame
import random
import utils
import copy
import Button
from queue import PriorityQueue

from search import bfs, ucs, AStar, Greedy, dfs, ids, Hill_Climbing
from Snake import Snake
from Square import Square
from Point import Point


class Game:
    BACKGROUND_COLOR = utils.BACKGROUND_COLOR
    FOOD_IMAGE = utils.FOOD_IMAGE
    DANGER_IMAGE = utils.DANGER_IMAGE
    PAUSE_IMAGE = utils.PAUSE_IMAGE
    RESUME_IMAGE = utils.RESUME_IMAGE
    BACK_IMAGE = utils.BACK_IMAGE
    VISUALIZE_IMAGE = utils.VISUALIZE_IMAGE
    HEIGHT = utils.HEIGHT
    WIDTH = utils.WIDTH
    SCREEN_HEIGHT = utils.SCREEN_HEIGHT
    SCREEN_WIDTH = utils.SCREEN_WIDTH
    game_state = "menu"  # Thêm trạng thái menu
    PLAYER_MODE = "player"
    AI_MODE = "AI"
    MAP_MODE = "map"
    RANK_MODE = "rank"
    current_mode = None  # Chế độ người chơi hiện tại
    algorithm = None
    bg = pygame.transform.scale(pygame.image.load('assets/bg_game.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    score_bg = pygame.transform.scale(pygame.image.load('assets/score_bg.png'), (330, SCREEN_HEIGHT))
    score_area = pygame.Surface((330 , SCREEN_HEIGHT))
    score_area.blit(score_bg, (0, 0))
    playing_area = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def __init__(self):
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH + 330, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")

        pygame.font.init()
        self.__font = pygame.font.Font(pygame.font.get_default_font(), 40)

        self.__clock = pygame.time.Clock()
        self.__reset()

    def run(self):
        while True:
            pygame.time.delay(20)
            self.__handle_events()
            if self.game_state == "menu":
                self.draw_menu()
            elif self.game_state == "game":
                if self.current_mode == self.PLAYER_MODE:
                    if self.pause == False:
                        if self.pause == False:
                            self.__handle_player_game()
                elif self.current_mode == self.AI_MODE:
                    if self.algorithm is None:
                        self.draw_algorithm_menu()
                    else:
                        self.__draw()
                        if self.pause == False:
                            self.AI_move()
            elif self.game_state == "map":
                self.draw_map_menu()
                self.create_map()
            elif self.game_state == "rank":
                self.draw_rank_table("rank.txt")
    def draw_rank_table(self, file_path):
        leaderboard_data = []
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if "algorithm" in line and "score" in line:
                        algorithm = line.split("algorithm:")[1].split("-")[0].strip()
                        score = int(line.split("score:")[1].strip())
                        leaderboard_data.append((algorithm, score))
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")

        self.screen.blit(utils.RANK_IMAGE, (0,0))  # White background
        font = pygame.font.Font(pygame.font.get_default_font(), 25)
        y_position = 200
        for entry in leaderboard_data:
            text = f"{entry[0]} - Score: {entry[1]}"
            rendered_text = font.render(text, True, (0, 0, 0))  # Black text
            self.screen.blit(rendered_text, (50, y_position))
            y_position += 40

        self.score_area.blit(self.score_bg, (0, 0))
        rank_label = font.render(f'RANK', True, '#000000')
        self.score_area.blit(rank_label, (10, 50))
        # Back label
        back_label = font.render(f'Back home:', True, '#000000')
        self.score_area.blit(back_label, (10, 100))
        # Back button
        self.score_area.blit(self.BACK_IMAGE, Button.back_button_in_rank)
        self.screen.blit(self.score_area, (self.SCREEN_WIDTH, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                self.game_state = "menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    back_button_pos = self.BACK_IMAGE.get_rect()
                    back_button_pos.topleft = (self.SCREEN_WIDTH + utils.BACK_POSITION_IN_RANK[0],
                                               utils.BACK_POSITION_IN_RANK[1])
                    if back_button_pos.collidepoint(event.pos[0], event.pos[1]):
                        self.game_state = "menu"
                        self.draw_menu()

    def save_score(self, filename, algo, score):
        if algo is None:
            print(algo)
            algo = "Human"
        with open(filename, 'a') as file:
            file.write(f"algorithm: {algo} - score: {score}\n")
        file.close()
    def clear_score(self,filename):
        f = open(filename, 'r+')
        f.truncate(0)
        f.close()

    def draw_map_menu(self):
        self.playing_area.fill(self.BACKGROUND_COLOR)
        self.screen.blit(self.playing_area, (0, 0))

        self.score_area.blit(self.score_bg, (0, 0))
        font = pygame.font.Font(pygame.font.get_default_font(), 25)

        ins_label = font.render(f'Click on map to draw', True, '#000000')
        self.score_area.blit(ins_label, (10, 50))

        del_label = font.render('Click on danger to delete', True, '#000000')
        self.score_area.blit(del_label, (10, 100))
        # Save label
        save_label = font.render(f'Save: ', True, '#000000')
        self.score_area.blit(save_label, (10, 150))
        # Save button
        self.score_area.blit(utils.SAVE_IMAGE, Button.save_button_pos)

        # Back label
        back_label = font.render(f'Back home:', True, '#000000')
        self.score_area.blit(back_label, (10, 200))
        # Back button
        self.score_area.blit(self.BACK_IMAGE, Button.back_button_rect)
        # Clear label
        clear_label = font.render(f'Clear map:', True, '#000000')
        self.score_area.blit(clear_label, (10, 250))
        # Clear button
        self.score_area.blit(utils.CLEAR_IMAGE, Button.clear_button_in_rank)

        self.screen.blit(self.score_area, (self.SCREEN_WIDTH, 0))
        self.__draw_dangers()

    def save_coordinates(self, filename, coordinates):
        with open(filename, 'w') as file:
            for coord in coordinates:
                file.write(f"{coord[0]}, {coord[1]}\n")
        file.close()

    def erase_square(self, x, y):
        pygame.draw.rect(self.screen, (246, 229, 141),
                         (x, y, Square.SQUARE_TOTAL_SIDE_LENGTH, Square.SQUARE_TOTAL_SIDE_LENGTH))
    def draw_square(self, x, y):
        #pygame.draw.rect(self.screen, (255,0,0), (x, y,Square.SQUARE_TOTAL_SIDE_LENGTH, Square.SQUARE_TOTAL_SIDE_LENGTH))
        square_image = self.DANGER_IMAGE
        square = square_image.get_rect()
        square.topleft = (x, y)
        self.screen.blit(square_image, square)
    def create_map(self):
        running = True
        drawing = False
        saved_coordinates = []
        saved_coordinates += self.__dangers_point
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.game_state = "menu"
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        a = (x + Square.SQUARE_BORDER_WIDTH) // Square.SQUARE_TOTAL_SIDE_LENGTH
                        b = (y + Square.SQUARE_BORDER_WIDTH) // Square.SQUARE_TOTAL_SIDE_LENGTH
                        if (a, b) in saved_coordinates:
                            saved_coordinates.remove((a, b))
                            self.erase_square(x - Square.SQUARE_TOTAL_SIDE_LENGTH // 2,
                                         y - Square.SQUARE_TOTAL_SIDE_LENGTH // 2)
                        elif x <= self.SCREEN_WIDTH and y <= self.SCREEN_HEIGHT:
                            saved_coordinates.append((a, b))
                            drawing = True
                        elif self.back_menu(event):
                            self.game_state = "menu"
                            self.draw_menu()
                            return
                        elif self.save_map(event, saved_coordinates):
                            self.save_coordinates("coordinates.txt", saved_coordinates)
                            self.clear_score("rank.txt")
                        elif self.clear_map(event):
                            saved_coordinates.clear()
                            self.playing_area.fill(self.BACKGROUND_COLOR)
                            self.screen.blit(self.playing_area, (0, 0))

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if drawing:
                            drawing = False
                            self.draw_square(x - Square.SQUARE_TOTAL_SIDE_LENGTH // 2,
                                         y - Square.SQUARE_TOTAL_SIDE_LENGTH // 2)

            pygame.display.update()

    def clear_map(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clear_button_pos = utils.CLEAR_IMAGE.get_rect()
                clear_button_pos.topleft = (self.SCREEN_WIDTH + utils.CLEAR_POSITION[0],
                                            utils.CLEAR_POSITION[1])
                if clear_button_pos.collidepoint(event.pos[0], event.pos[1]):
                    return True

    def save_map(self, event, saved_coordinates):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                save_button_pos = utils.SAVE_IMAGE.get_rect()
                save_button_pos.topleft = (self.SCREEN_WIDTH + utils.SAVE_POSITION[0],
                                            utils.SAVE_POSITION[1])
                if save_button_pos.collidepoint(event.pos[0], event.pos[1]):
                    return True
        return False
    def AI_move(self):
        head = (self.__snake.squares[-1].position.x, self.__snake.squares[-1].position.y)
        # type head is tuple
        food = (self.__food.position.x, self.__food.position.y)
        body = tuple(self.__snake.squares)
        if self.algorithm == "bfs":
            way, self.__visualization = bfs(head, food, self.__snake.direction["name"], body, self.__dangers_set)
        elif self.algorithm == "ucs":
            way, self.__visualization = ucs(head, food, self.__snake.direction["name"], body, self.__dangers_set)
        elif self.algorithm == "astar":
            way, self.__visualization = AStar(head, food, self.__snake.direction["name"], body, self.__dangers_set)
        elif self.algorithm == "greedy":
            way, self.__visualization = Greedy(head, food, self.__snake.direction["name"], body, self.__dangers_set)
        elif self.algorithm == "dfs":
            _, way, self.__visualization = dfs(head, food, self.__snake.direction["name"], body, self.__dangers_set)
        elif self.algorithm == "ids":
            way, self.__visualization = ids(head, food, self.__snake.direction["name"], body, self.__dangers_set)
        if self.algorithm == "hill":
            way, self.__visualization, self.__cannot_choose = \
                Hill_Climbing(head, food, self.__snake.direction["name"], body, self.__dangers_set)
        self.__auto_move(way)

    def __reset(self):
        self.__score = 0
        self.algorithm = None
        self.__direction_key = None
        self.__snake = Snake(Point(self.WIDTH / 2, self.HEIGHT / 2))
        self.__generate_danger()
        self.__generate_food()
        self.__visualization = set()
        self.__cannot_choose = set()
        self.pause = False
        self.visualize_mode = False

    def __generate_danger(self):
        self.__dangers_point = []
        self.__dangers = []
        saved_coordinates = []
        self.__dangers_set = set()
        with open('coordinates.txt', 'r') as file:
            lines = file.readlines()
        for line in lines:
            x, y = map(float, line.split(','))
            self.__dangers_point.append((x,y))
            danger = Square(self.DANGER_IMAGE, Point(x, y))
            self.__dangers.append(danger)
            self.__dangers_set.add((danger.position.x, danger.position.y))
        # for i in range(10):
        #     while (True):
        #         x = random.randrange(3, self.WIDTH - 3)
        #         y = random.randrange(3, self.HEIGHT - 3)
        #         danger = Square(self.DANGER_IMAGE, Point(x, y))
        #         if danger not in self.__dangers:
        #             self.__dangers.append(danger)
        #             saved_coordinates.append((x, y))
        #             self.__dangers_set.add((danger.position.x, danger.position.y))
        #             break
        # self.save_coordinates("coordinates.txt", saved_coordinates)

    def __draw_dangers(self):
        for danger in self.__dangers:
            danger.draw_image(self.screen)

    def __generate_food(self):
        self.__food = Square(self.FOOD_IMAGE,
                             Point(random.randrange(2, self.WIDTH - 2), random.randrange(2, self.HEIGHT - 2)))
        while self.__food in self.__snake.squares or \
                (self.__food.position.x, self.__food.position.y) in self.__dangers_set:
            self.__food = Square(self.FOOD_IMAGE,
                                 Point(random.randrange(2, self.WIDTH - 2), random.randrange(2, self.HEIGHT - 2)))

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.resume_game(event):
                        self.pause = False
                        self.PAUSE_IMAGE = utils.PAUSE_IMAGE
                    elif self.back_menu(event):
                        self.game_state = "menu"
                        self.PAUSE_IMAGE = utils.PAUSE_IMAGE
                        self.draw_menu()
                    elif self.visualize(event):
                        if self.visualize_mode:
                            self.visualize_mode = False
                            self.VISUALIZE_IMAGE = utils.VISUALIZE_IMAGE
                        else:
                            self.visualize_mode = True
                            self.VISUALIZE_IMAGE = utils.UNVISUALIZE_IMAGE
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "menu":
                    if event.key == pygame.K_1:
                        self.game_state = "game"
                        self.current_mode = self.PLAYER_MODE
                        self.__reset()
                    elif event.key == pygame.K_2:
                        self.game_state = "game"
                        self.current_mode = self.AI_MODE
                        self.__reset()
                    elif event.key == pygame.K_3:
                        self.game_state = "map"
                        self.current_mode = self.MAP_MODE
                        self.__reset()
                    elif event.key == pygame.K_4:
                        self.game_state = "rank"
                        self.current_mode = self.RANK_MODE
                        self.__reset()
                elif self.game_state == "game_over_menu":
                    if event.key == pygame.K_SPACE:
                        self.game_state = "menu"
                        self.current_mode = None
                        self.__reset()
                elif self.game_state == "game_over":
                    if event.key == pygame.K_SPACE:
                        self.save_score("rank.txt", self.algorithm, self.__score)
                        self.draw_game_over()
                        self.game_state = "game_over_menu"
                elif self.game_state == "game" and self.algorithm is None:
                    self.VISUALIZE_IMAGE = utils.VISUALIZE_IMAGE
                    if event.key == pygame.K_0:
                        self.game_state = "menu"
                    if event.key == pygame.K_1:
                        self.algorithm = "bfs"
                    if event.key == pygame.K_2:
                        self.algorithm = "dfs"
                    if event.key == pygame.K_3:
                        self.algorithm = "ids"
                    if event.key == pygame.K_4:
                        self.algorithm = "astar"
                    if event.key == pygame.K_5:
                        self.algorithm = "greedy"
                    if event.key == pygame.K_6:
                        self.algorithm = "ucs"
                    if event.key == pygame.K_7:
                        self.algorithm = "hill"

                elif self.__snake.is_alive:
                    if event.key in Snake.DIRECTIONS:
                        self.__direction_key = event.key
                elif not self.__snake.is_alive:
                    self.game_state = "game_over"

    def __handle_player_game(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.__snake.direction["name"] != "right":
            self.__direction_key = pygame.K_LEFT
        if keys[pygame.K_RIGHT] and self.__snake.direction["name"] != "left":
            self.__direction_key = pygame.K_RIGHT
        if keys[pygame.K_UP] and self.__snake.direction["name"] != "down":
            self.__direction_key = pygame.K_UP
        if keys[pygame.K_DOWN] and self.__snake.direction["name"] != "up":
            self.__direction_key = pygame.K_DOWN

        self.__clock.tick(utils.SPEED)
        self.__tick()
        self.__draw()

    def __auto_move(self, way):
        for char in way:
            if char == "l":
                self.__direction_key = pygame.K_LEFT
            if char == "r":
                self.__direction_key = pygame.K_RIGHT
            if char == "u":
                self.__direction_key = pygame.K_UP
            if char == "d":
                self.__direction_key = pygame.K_DOWN
            for event in pygame.event.get():
                if self.back_menu(event):
                    self.game_state = "menu"
                    self.draw_menu()
                    return
                elif self.pause_game(event):
                    self.pause = True
                    self.PAUSE_IMAGE = utils.RESUME_IMAGE
                    return
                elif self.visualize(event):
                    if self.visualize_mode:
                        self.visualize_mode = False
                        self.VISUALIZE_IMAGE = utils.VISUALIZE_IMAGE
                    else:
                        self.visualize_mode = True
                        self.VISUALIZE_IMAGE = utils.UNVISUALIZE_IMAGE
            self.__clock.tick(utils.SPEED)
            self.__tick()
            self.__draw()

    def visualize(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                vis_button_pos = self.VISUALIZE_IMAGE.get_rect()
                vis_button_pos.topleft = (self.SCREEN_WIDTH + utils.VISUALIZE_POSITION[0],
                                            utils.VISUALIZE_POSITION[1])
                if vis_button_pos.collidepoint(event.pos[0], event.pos[1]):
                    return True
        return False

    def back_menu(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                back_button_pos = self.BACK_IMAGE.get_rect()
                back_button_pos.topleft = (self.SCREEN_WIDTH + utils.BACK_POSITION[0],
                                            utils.BACK_POSITION[1])
                if back_button_pos.collidepoint(event.pos[0], event.pos[1]):
                    return True
        return False
    def pause_game(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if Button.pause_button_pos.collidepoint(event.pos[0], event.pos[1]):
                    return True
        return False
    def resume_game(self, event):
        if Button.pause_button_pos.collidepoint(event.pos[0], event.pos[1]):
            return True
        return False

    def __tick(self):
        if self.__snake.is_alive:
            snake_pos = self.__snake.move(self.__direction_key)
            if (snake_pos.x, snake_pos.y) in self.__dangers_set:
                self.__snake.is_alive = False
                self.game_state = "game_over"
                return
            if snake_pos == self.__food.position:
                self.__score += 1
                self.__generate_food()
            else:
                self.__snake.shrink()
        else:
            self.game_state = "game_over"

    def __draw(self):
        # Draw playing area
        self.playing_area.fill(self.BACKGROUND_COLOR)
        if self.visualize_mode:
            for x, y in self.__cannot_choose:
                Square('', Point(x, y)).draw(self.playing_area, '#e74c3c')
            for x, y in self.__visualization:
                Square('', Point(x, y)).draw(self.playing_area, '#ffffff')
        self.__snake.draw(self.playing_area)
        self.__food.draw_image(self.playing_area)

        # Draw score area
        self.score_area.blit(self.score_bg, (0, 0))
        font = pygame.font.Font(pygame.font.get_default_font(), 25)

        score_label = font.render(f'Score: {self.__score}', True, '#000000')
        self.score_area.blit(score_label, (10, 50))

        algo_label = font.render(f'Algorithm: {self.algorithm}', True, '#000000')
        self.score_area.blit(algo_label, (10, 100))

        # Pause label
        pause_label = font.render(f'Pause/Resume:', True, '#000000')
        self.score_area.blit(pause_label, (10, 150))
        # Pause button
        self.score_area.blit(self.PAUSE_IMAGE, Button.pause_button_pos_on_score_area)

        #Back label
        back_label = font.render(f'Back home:', True, '#000000')
        self.score_area.blit(back_label, (10, 200))
        #Back button
        self.score_area.blit(self.BACK_IMAGE, Button.back_button_rect)

        # visualize label
        visualize_label = font.render(f'Visualize:', True, '#000000')
        self.score_area.blit(visualize_label, (10, 250))
        # visualize button
        self.score_area.blit(self.VISUALIZE_IMAGE, Button.visualize_button_rect)

        # Blit both areas to the main screen
        self.screen.blit(self.playing_area, (0, 0))
        self.__draw_dangers()
        self.screen.blit(self.score_area, (self.SCREEN_WIDTH, 0))

        # Display game over message if applicable
        if not self.__snake.is_alive:
            text_label = self.__font.render("Press Space to continue and save score", 1, '#000000')
            self.screen.blit(text_label, (self.SCREEN_WIDTH / 2 - text_label.get_width() / 2, 500))

        pygame.display.update()

    def draw_menu(self):
        bg = pygame.image.load('assets/background.jpg')
        bg = pygame.transform.scale(bg, (self.SCREEN_WIDTH + 330, self.SCREEN_HEIGHT))

        self.screen.blit(bg, (0, 0))
        font = pygame.font.SysFont('arial', 40)
        title = font.render('Snake Game', True, (0, 100, 0))
        player_mode = font.render('1. Player Mode', True, (0, 100, 0))
        AI_mode = font.render('2. AI Mode', True, (0, 100, 0))
        Map_mode = font.render('3. Create map', True, (0, 100, 0))
        Ranking_mode = font.render('4. Rank', True, (0, 100, 0))
        self.screen.blit(title, (
            self.SCREEN_WIDTH / 2 - title.get_width() / 2 + 150, self.SCREEN_HEIGHT / 2 - title.get_height() / 3))
        self.screen.blit(player_mode, (
            self.SCREEN_WIDTH / 2 - player_mode.get_width() / 2 + 150,
            self.SCREEN_HEIGHT / 2 + player_mode.get_height() / 2))
        self.screen.blit(AI_mode, (
            self.SCREEN_WIDTH / 2 - AI_mode.get_width() / 2 + 150, self.SCREEN_HEIGHT / 1.9 + AI_mode.get_height()))
        self.screen.blit(Map_mode, (
            self.SCREEN_WIDTH / 2 - Map_mode.get_width() / 2 + 150, self.SCREEN_HEIGHT / 1.7 + Map_mode.get_height()))
        self.screen.blit(Ranking_mode, (
            self.SCREEN_WIDTH / 2 - Ranking_mode.get_width() / 2 + 150, self.SCREEN_HEIGHT / 1.5 + Ranking_mode.get_height()))
        pygame.display.update()

    def draw_game_over(self):
        self.screen.fill((138, 169, 3))
        font = pygame.font.SysFont('arial', 40)
        game_over_label = font.render('Game Over', True, (0, 100, 0))
        score_label = font.render(f'Score: {self.__score}', True, (0, 100, 0))
        restart_label = font.render('Press Space to Restart', True, (0, 100, 0))
        self.screen.blit(game_over_label, (
            self.SCREEN_WIDTH / 2 - game_over_label.get_width() / 2 + 150,
            self.SCREEN_HEIGHT / 2 - game_over_label.get_height()))
        self.screen.blit(score_label, (
            self.SCREEN_WIDTH / 2 - score_label.get_width() / 2 + 150,
            self.SCREEN_HEIGHT / 1.9 + score_label.get_height()))
        self.screen.blit(restart_label, (
            self.SCREEN_WIDTH / 2 - restart_label.get_width() / 2 + 150,
            self.SCREEN_HEIGHT / 2 + restart_label.get_height() / 2))
        pygame.display.update()

    def draw_algorithm_menu(self):
        bg = pygame.image.load('assets/background.jpg')
        bg = pygame.transform.scale(bg, (self.SCREEN_WIDTH + 330, self.SCREEN_HEIGHT))

        self.screen.blit(bg, (0, 0))
        font_size = 40
        font = pygame.font.SysFont('arial', font_size)

        algorithm_options = ['1. BFS', '2. DFS', '3. IDS', '4. A star', '5. Greedy', '6. UCS', '7. Hill Climbing',
                             '0. Back']
        total_options = len(algorithm_options)
        rows = 4
        cols = 2
        horizontal_space = self.SCREEN_WIDTH / (cols + 1)
        vertical_space = self.SCREEN_HEIGHT / (rows + 1)

        for i, option in enumerate(algorithm_options, start=1):
            row = (i - 1) // cols
            col = (i - 1) % cols

            text_render = font.render(option, True, (0, 100, 0))
            text_position = (
                col * horizontal_space + 20,  # Căn lề bên trái
                row * vertical_space + vertical_space - text_render.get_height() / 2)
            self.screen.blit(text_render, text_position)

        pygame.display.update()