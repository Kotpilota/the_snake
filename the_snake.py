import pygame
from random import randint

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона, границ ячейки, яблока и змейки
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)


# Скорость движения змейки
SNAKE_SPEED = 20

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """Инициализирует объект."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки, предназначен для дочерних классов."""
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        """Инициализирует яблоко и устанавливает его позицию."""
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Генерирует случайное положение яблока."""
        x_position = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y_position = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x_position, y_position)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        apple_rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, apple_rect)
        pygame.draw.rect(screen, BORDER_COLOR, apple_rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Инициализирует змейку с начальным данными."""
        super().__init__(
            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            body_color=SNAKE_COLOR
        )
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last_segment_position = None

    def update_direction(self):
        """Обновляет направление змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет положение змейки на экране."""
        head_x, head_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_head_position = (
            (head_x + delta_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + delta_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.last_segment_position = self.positions.pop()
        else:
            self.last_segment_position = None

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            segment_rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, segment_rect)
            pygame.draw.rect(screen, BORDER_COLOR, segment_rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last_segment_position:
            last_rect = pygame.Rect(
                self.last_segment_position,
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(
                screen,
                BOARD_BACKGROUND_COLOR,
                last_rect
            )

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс змейки до её начального состояния."""
        self.__init__()


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif (event.key == pygame.K_DOWN
                  and snake.direction != UP):
                snake.next_direction = DOWN
            elif (event.key == pygame.K_LEFT
                  and snake.direction != RIGHT):
                snake.next_direction = LEFT
            elif (event.key == pygame.K_RIGHT
                  and snake.direction != LEFT):
                snake.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SNAKE_SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()

# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP
#             and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN
#             and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT
#             and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT
#             and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
