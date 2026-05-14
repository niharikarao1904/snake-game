import turtle
import random
import time

# Screen setup
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Colors
BG_COLOR = "#1a1a2e"
SNAKE_HEAD_COLOR = "#00ff88"
SNAKE_BODY_COLOR = "#00cc6a"
FOOD_COLOR = "#ff6b6b"
BORDER_COLOR = "#4a4a6a"
TEXT_COLOR = "#ffffff"
GAME_OVER_COLOR = "#ff6b6b"

# Game settings
INITIAL_DELAY = 150
MIN_DELAY = 80
SPEED_DECREASE = 2
POINTS_PER_FOOD = 10
INITIAL_SNAKE_LENGTH = 3


class SnakeGame:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Snake Game")
        self.screen.setup(WINDOW_WIDTH + 40, WINDOW_HEIGHT + 80)
        self.screen.bgcolor(BG_COLOR)
        self.screen.tracer(0)

        # Game state
        self.snake = []
        self.direction = (1, 0)  # Start moving right
        self.next_direction = (1, 0)
        self.food = None
        self.score = 0
        self.high_score = 0
        self.game_running = False
        self.paused = False
        self.game_over = False

        # Turtle objects
        self.snake_segments = []
        self.food_turtle = None
        self.score_turtle = None
        self.high_score_turtle = None
        self.message_turtle = None

        self.setup_game()
        self.setup_controls()

        self.screen.mainloop()

    def setup_game(self):
        # Draw border
        border = turtle.Turtle()
        border.penup()
        border.hideturtle()
        border.color(BORDER_COLOR)
        border.pensize(3)
        border.goto(-WINDOW_WIDTH // 2 + 10, WINDOW_HEIGHT // 2 - 10)
        border.pendown()
        for _ in range(4):
            if _ % 2 == 0:
                border.forward(WINDOW_WIDTH - 20)
            else:
                border.forward(WINDOW_HEIGHT - 20)
            border.right(90)

        # Score display
        self.score_turtle = turtle.Turtle()
        self.score_turtle.penup()
        self.score_turtle.hideturtle()
        self.score_turtle.color(TEXT_COLOR)
        self.score_turtle.goto(-WINDOW_WIDTH // 2 + 30, WINDOW_HEIGHT // 2 - 40)
        self.score_turtle.write("Score: 0", font=("Courier", 16, "bold"))

        # High score display
        self.high_score_turtle = turtle.Turtle()
        self.high_score_turtle.penup()
        self.high_score_turtle.hideturtle()
        self.high_score_turtle.color("#ffd700")
        self.high_score_turtle.goto(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 40)
        self.high_score_turtle.write("High Score: 0", font=("Courier", 16, "bold"))

        # Message display (pause/game over)
        self.message_turtle = turtle.Turtle()
        self.message_turtle.penup()
        self.message_turtle.hideturtle()
        self.message_turtle.color(TEXT_COLOR)

        # Initialize snake
        self.init_snake()

        # Spawn initial food
        self.spawn_food()

        # Start game
        self.game_running = True
        self.paused = False
        self.game_over = False

        # Start game loop
        self.update()

    def init_snake(self):
        # Clear existing segments
        for segment in self.snake_segments:
            segment.hideturtle()
        self.snake_segments.clear()

        # Create snake at center
        start_x = 0
        start_y = 0
        self.snake = []
        for i in range(INITIAL_SNAKE_LENGTH):
            x = start_x - i * CELL_SIZE
            y = start_y
            self.snake.append((x, y))

        # Create turtle segments
        for i, (x, y) in enumerate(self.snake):
            segment = turtle.Turtle()
            segment.shape("square")
            segment.penup()
            if i == 0:
                segment.color(SNAKE_HEAD_COLOR)
            else:
                # Gradient effect - darker towards tail
                shade = max(0.3, 1 - (i / len(self.snake)) * 0.7)
                r = int(0 * shade)
                g = int(204 * shade)
                b = int(106 * shade)
                segment.color(f"#{r:02x}{g:02x}{b:02x}")
            segment.goto(x, y)
            self.snake_segments.append(segment)

    def spawn_food(self):
        # Find valid position (not on snake)
        while True:
            x = random.randint(-GRID_WIDTH // 2 + 1, GRID_WIDTH // 2 - 1) * CELL_SIZE
            y = random.randint(-GRID_HEIGHT // 2 + 1, GRID_HEIGHT // 2 - 1) * CELL_SIZE
            if (x, y) not in self.snake:
                break

        self.food = (x, y)

        if self.food_turtle:
            self.food_turtle.hideturtle()

        self.food_turtle = turtle.Turtle()
        self.food_turtle.shape("circle")
        self.food_turtle.color(FOOD_COLOR)
        self.food_turtle.penup()
        self.food_turtle.goto(x, y)
        self.food_turtle.shapesize(0.8, 0.8)

    def setup_controls(self):
        self.screen.listen()

        # Direction controls
        self.screen.onkeypress(lambda: self.change_direction(0, 1), "Up")
        self.screen.onkeypress(lambda: self.change_direction(0, 1), "w")
        self.screen.onkeypress(lambda: self.change_direction(0, -1), "Down")
        self.screen.onkeypress(lambda: self.change_direction(0, -1), "s")
        self.screen.onkeypress(lambda: self.change_direction(-1, 0), "Left")
        self.screen.onkeypress(lambda: self.change_direction(-1, 0), "a")
        self.screen.onkeypress(lambda: self.change_direction(1, 0), "Right")
        self.screen.onkeypress(lambda: self.change_direction(1, 0), "d")

        # Pause control
        self.screen.onkeypress(self.toggle_pause, "space")

        # Restart control
        self.screen.onkeypress(self.restart_game, "r")

    def change_direction(self, dx, dy):
        # Prevent reversing direction
        if self.game_over or self.paused:
            return

        # Can't reverse: (dx, dy) + current direction = (0, 0)
        if dx == -self.direction[0] and dy == -self.direction[1]:
            return
        if dx == 0 and dy == 0:
            return

        self.next_direction = (dx, dy)

    def toggle_pause(self):
        if self.game_over:
            return

        self.paused = not self.paused

        if self.paused:
            self.message_turtle.goto(0, 0)
            self.message_turtle.color(TEXT_COLOR)
            self.message_turtle.write("PAUSED\nPress SPACE to continue", align="center", font=("Courier", 20, "bold"))
        else:
            self.message_turtle.clear()
            self.update()

    def move_snake(self):
        # Update direction
        self.direction = self.next_direction

        # Calculate new head position
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0] * CELL_SIZE, head_y + self.direction[1] * CELL_SIZE)

        # Check wall collision
        half_width = WINDOW_WIDTH // 2 - CELL_SIZE
        half_height = WINDOW_HEIGHT // 2 - CELL_SIZE
        if abs(new_head[0]) > half_width or abs(new_head[1]) > half_height:
            self.end_game()
            return

        # Check self collision
        if new_head in self.snake:
            self.end_game()
            return

        # Add new head
        self.snake.insert(0, new_head)

        # Check food collision
        if new_head == self.food:
            # Eat food
            self.score += POINTS_PER_FOOD
            self.update_score()
            self.spawn_food()
            # Don't remove tail - snake grows
        else:
            # Remove tail
            tail = self.snake.pop()
            tail_segment = self.snake_segments.pop()
            tail_segment.hideturtle()

        # Update turtle positions
        self.update_snake_graphics()

    def update_snake_graphics(self):
        for i, (x, y) in enumerate(self.snake):
            if i < len(self.snake_segments):
                self.snake_segments[i].goto(x, y)
            else:
                # Create new segment
                segment = turtle.Turtle()
                segment.shape("square")
                segment.penup()
                shade = max(0.3, 1 - (i / len(self.snake)) * 0.7)
                r = int(0 * shade)
                g = int(204 * shade)
                b = int(106 * shade)
                segment.color(f"#{r:02x}{g:02x}{b:02x}")
                segment.goto(x, y)
                self.snake_segments.append(segment)

        # Ensure head is colored correctly
        if self.snake_segments:
            self.snake_segments[0].color(SNAKE_HEAD_COLOR)

    def update_score(self):
        self.score_turtle.clear()
        self.score_turtle.write(f"Score: {self.score}", font=("Courier", 16, "bold"))

        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_turtle.clear()
            self.high_score_turtle.write(f"High Score: {self.high_score}", font=("Courier", 16, "bold"))

    def end_game(self):
        self.game_running = False
        self.game_over = True

        # Show game over message
        self.message_turtle.goto(0, -30)
        self.message_turtle.color(GAME_OVER_COLOR)
        self.message_turtle.write(f"GAME OVER\nFinal Score: {self.score}\nPress R to restart", align="center", font=("Courier", 24, "bold"))

    def restart_game(self):
        if not self.game_over:
            return

        # Reset game state
        self.score = 0
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.game_over = False

        # Clear message
        self.message_turtle.clear()

        # Reinitialize
        self.init_snake()
        self.spawn_food()
        self.update_score()

        # Start game
        self.game_running = True
        self.update()

    def get_delay(self):
        # Speed increases with score
        delay = INITIAL_DELAY - (self.score // POINTS_PER_FOOD) * SPEED_DECREASE
        return max(MIN_DELAY, delay)

    def update(self):
        if not self.game_running:
            return

        if not self.paused and not self.game_over:
            self.move_snake()

            if not self.game_over:
                self.screen.update()
                delay = self.get_delay()
                self.screen.ontimer(self.update, delay)


if __name__ == "__main__":
    SnakeGame()
