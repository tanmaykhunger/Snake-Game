from tkinter import *
import random

# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 80
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:
    """
    Represents the snake in the game.
    """

    def __init__(self):
        """
        Initializes a new instance of the Snake class.

        The snake's initial attributes are set, including body size, coordinates, and squares.
        """
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


class Food:
    """
    Represents the food item in the game.
    """

    def __init__(self):
        """
        Initializes a new instance of the Food class.

        The food's coordinates attribute is randomly generated within the game grid, and the food item is created on the canvas.
        """
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )


def next_turn(snake, food):
    """
    Performs the next turn in the game.

    Args:
        snake (Snake): The snake object representing the player-controlled snake.
        food (Food): The food object representing the food item.

    This function updates the game state, including the snake's position and checks for collisions or game over conditions.
    """
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    """
    Changes the direction of the snake based on user input.

    Args:
        new_direction (str): The new direction of the snake. Valid values are 'left', 'right', 'up', and 'down'.
    """
    global direction

    if new_direction == "left":
        if direction != "right":
            direction = new_direction

    elif new_direction == "right":
        if direction != "left":
            direction = new_direction

    elif new_direction == "up":
        if direction != "down":
            direction = new_direction

    elif new_direction == "down":
        if direction != "up":
            direction = new_direction


def check_collisions(snake):
    """
    Checks for collisions between the snake and other game objects.

    Args:
        snake (Snake): The snake object representing the player-controlled snake.

    Returns:
        bool: True if a collision is detected, False otherwise.

    This function checks for collisions between the snake's head, its body, and the game boundaries or food item.
    """
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True

    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True

    return False


def game_over():
    """
    Handles the game over state.

    This function is called when the game is over. It clears the canvas and displays the game over message.
    """
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=("consoles", 70),
        text="GAME OVER",
        fill="red",
        tag="gameover",
    )


# Create the main window
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

# Initialize variables
score = 0
direction = "down"

# Create score label
label = Label(window, text="Score:{}".format(score), font=("consoles", 40))
label.pack()

# Create game canvas
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Set window position
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))

# Bind arrow keys to change direction
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

# Create snake and food objects
snake = Snake()
food = Food()

# Start the game loop
next_turn(snake, food)

# Run the main window event loop
window.mainloop()
