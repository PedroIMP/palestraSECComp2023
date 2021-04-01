import random

WIDTH = 500
HEIGHT = 500

BLOCK_LENGTH = 20

BLOCKS_X = WIDTH // BLOCK_LENGTH
BLOCKS_Y = HEIGHT // BLOCK_LENGTH

class Snake:
    def __init__(self):
        # Blocks composing the body of the snake.
        # Each element is a block (x, y) pair.
        self.body = [(0, 0)]
        
        # Current (x, y) direction of the snake.
        # Possible values: (1, 0), (0, 1), (-1, 0), (0, -1)
        self.direction = (1, 0)
        
        self.direction_buffer = []
        
        # Current speed of the snake in
        # blocks per second
        self.speed = 7
        
        # Elapsed time since last update
        self.dt = 0
    
    def set_direction(self, direction):
        if direction not in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            return
        
        cur_x, cur_y = self.direction_buffer[-1] if self.direction_buffer else self.direction
            
        x, y = direction
        if x + cur_x == 0 or y + cur_y == 0:
            return
        
        self.direction_buffer.append((x, y))
    
    def update(self, dt):
        self.dt += dt
        delta = int(self.speed * self.dt)
        self.dt %= 1 / self.speed
        while delta:
            if self.direction_buffer:
                self.direction = self.direction_buffer.pop(0)
            x, y = self.body[-1]
            dir_x, dir_y = self.direction
            x = (x + dir_x) % BLOCKS_X
            y = (y + dir_y) % BLOCKS_Y
            self.body.append((x, y))
            self.body.pop(0)
            delta -= 1
            
    def grow(self):
        dir_x, dir_y = self.direction
        if len(self.body) > 1:
            dir_x = self.body[1][0] - self.body[0][0]
            dir_y = self.body[1][1] - self.body[0][1]
            
        new_block = (self.body[0][0] - dir_x, self.body[0][1] - dir_y)
        self.body.insert(0, new_block)
        
    def draw(self):
        for x, y in self.body:
            r = Rect((x * BLOCK_LENGTH, y * BLOCK_LENGTH), (BLOCK_LENGTH, BLOCK_LENGTH))
            c = (255, 255, 255)
            screen.draw.filled_rect(r, c)


class Food:
    def __init__(self):
        self.x = BLOCKS_X // 2
        self.y = BLOCKS_Y // 2
    
    def draw(self):
        r = Rect((self.x * BLOCK_LENGTH, self.y * BLOCK_LENGTH), (BLOCK_LENGTH, BLOCK_LENGTH))
        c = (255, 0, 0)
        screen.draw.filled_rect(r, c)


snake = Snake()
food = Food()


def draw():
    screen.clear()
    snake.draw()
    food.draw()

def update(dt):
    snake.update(dt)
    snake_head = snake.body[-1]
    food_position = (food.x, food.y)
    
    if snake_head == food_position:
        snake.grow()
        while food_position in snake.body:
            x = random.randint(0, BLOCKS_X - 1)
            y = random.randint(0, BLOCKS_X - 1)
            food_position = x, y
        food.x, food.y = food_position
    
def on_key_down(key):
    direction = {
        keys.LEFT: (-1, 0),
        keys.RIGHT: (1, 0),
        keys.UP: (0, -1),
        keys.DOWN: (0, 1),
    }.get(key)
    
    if direction:
        snake.set_direction(direction)