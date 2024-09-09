import pygame
from random import randint

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Словарь для поворотов:
# ключ — (текущее направление, клавиша), значение — новое направление
DIRECTION_MAP = {
    (UP, pygame.K_LEFT): LEFT,
    (DOWN, pygame.K_LEFT): LEFT,
    (LEFT, pygame.K_UP): UP,
    (RIGHT, pygame.K_UP): UP,
    (UP, pygame.K_RIGHT): RIGHT,
    (DOWN, pygame.K_RIGHT): RIGHT,
    (LEFT, pygame.K_DOWN): DOWN,
    (RIGHT, pygame.K_DOWN): DOWN
}

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


class GameOver(Exception):
    """
    Custom exception to indicate the end of the game.

    This exception is raised when the game is over (e.g., when the player
    closes the game window). It is handled in the main game loop.
    """

    print('Player has quitted the game!')


class GameObject:
    """
    A base class for all game objects.

    Attributes:
        position (tuple): The (x, y) position of the object on the screen.
        body_color (tuple): The RGB color of the object.

    Methods:
        draw(): Method to be overridden by subclasses to draw the object on the screen.
    """

    def __init__(self, position=None, body_color=None):
        """
        Initializes the game object with a position and a color.

        Args:
            position (tuple): The initial position of the object (default is None).
            body_color (tuple): The color of the object (default is None).
        """
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Draws the game object on the screen. To be implemented by child classes."""
        pass


class Apple(GameObject):
    """
    Represents the apple in the game.

    The apple is a game object that can appear at a random position on the screen.
    The player must collect apples to grow the snake.

    Methods:
        randomize_position(): Randomly sets the position of the apple on the screen.
        draw(): Draws the apple on the screen.
    """

    def __init__(self):
        """Initializes the apple and sets its initial random position."""
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Generates a random position for the apple within the game grid."""
        x_position = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y_position = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x_position, y_position)

    def draw(self):
        """Draws the apple as a square on the screen."""
        apple_rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, apple_rect)
        pygame.draw.rect(screen, BORDER_COLOR, apple_rect, 1)


class Snake(GameObject):
    """
    Represents the snake in the game.

    The snake is the main character controlled by the player. It moves in a
    specified direction and grows in length when it eats an apple.

    Methods:
        update_direction(): Updates the snake's direction based on user input.
        move(): Moves the snake in the current direction.
        draw(): Draws the snake on the screen.
        get_head_position(): Returns the position of the snake's head.
        reset(): Resets the snake to its initial state.
    """

    def __init__(self):
        """Initializes the snake with a starting position, direction, and length."""
        super().__init__(
            position=SCREEN_CENTER,
            body_color=SNAKE_COLOR
        )
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last_segment_position = None

    def update_direction(self):
        """Updates the direction of the snake based on the next direction."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Moves the snake in the current direction.

        Calculates the new head position based on the current direction.
        The snake wraps around the screen edges.
        """
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
        """Draws the snake on the screen."""
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
        """Returns the current position of the snake's head."""
        return self.positions[0]

    def reset(self):
        """Resets the snake to its initial state: centered, single segment, moving right."""
        self.positions = [SCREEN_CENTER]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.last_segment_position = None


def handle_keys(snake):
    """
    Handles keyboard input to control the snake.

    Listens for key events to change the snake's direction or quit the game.
    If the Quit event is detected, raises the GameOver exception.

    Args:
        snake (Snake): The snake object whose direction will be controlled.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise GameOver
        elif event.type == pygame.KEYDOWN:
            new_direction = DIRECTION_MAP.get((snake.direction, event.key))
            if new_direction and new_direction != snake.direction:
                snake.next_direction = new_direction


def main():
    """
    The main game loop.

    Initializes the game, creates the snake and apple objects,
    and runs the game loop, handling user input, updating game
    state, and rendering graphics until the game is over.
    """
    pygame.init()
    snake = Snake()
    apple = Apple()

    try:
        while True:
            clock.tick(SNAKE_SPEED)
            handle_keys(snake)
            snake.update_direction()
            snake.move()

            # Check for collisions with apple or snake body
            if snake.get_head_position() == apple.position:
                snake.length += 1
                apple.randomize_position()

            if snake.get_head_position() in snake.positions[1:]:
                snake.reset()

            # Render the game state
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.draw()
            snake.draw()
            pygame.display.update()

    except GameOver:
        pygame.quit()


if __name__ == '__main__':
    main()
