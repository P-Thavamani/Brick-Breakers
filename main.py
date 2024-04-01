import pygame
import random
import pygame.mixer

pygame.init()

pygame.mixer.init()

# Dimensions of the screen
WIDTH, HEIGHT = 600, 500

# Load Sound Effects
block_hit_sound = pygame.mixer.Sound('BALL_HIT.wav')
background_music = pygame.mixer.Sound('BB_THEME.wav')
collision_sound = pygame.mixer.Sound('collision_sound.wav')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

font = pygame.font.Font('freesansbold.ttf', 15)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker")

# Create the game menu screen
def game_menu(screen, background_music, game_main):
    menu_running = True

    start_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 30, 100, 50)
    exit_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 30, 100, 50)

    background_music.play(loops=-1)

    while menu_running:
        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, WHITE, start_button)
        pygame.draw.rect(screen, WHITE, exit_button)

        start_text = font.render("Start", True, BLACK)
        start_text_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_text_rect)

        exit_text = font.render("Exit", True, BLACK)
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        screen.blit(exit_text, exit_text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    menu_running = False
                    background_music.stop()
                    main(screen)

                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    return



# to control the frame rate
clock = pygame.time.Clock()
FPS = 30


# Striker class
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.speed = speed
        self.color = color

        # The rect variable is used to handle the placement
        # and the collisions of the object
        self.strikerRect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        self.striker = pygame.draw.rect(screen,self.color, self.strikerRect)

    # Used to render the object on the screen
    def display(self):
        self.striker = pygame.draw.rect(screen,self.color, self.strikerRect)

    # Used to update the state of the object
    def update(self, xFac):
        self.posx += self.speed*xFac

        # Restricting the striker to be in between the
        # left and right edges of the screen
        if self.posx <= 0:
            self.posx = 0
        elif self.posx+self.width >= WIDTH:
            self.posx = WIDTH-self.width

        self.strikerRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    # Returns the rect of the object
    def getRect(self):
        return self.strikerRect


# Block Class
class Block:
    def __init__(self, posx, posy, width, height, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color
        self.damage = 100

        # The white blocks have the health of 200. So,
        # the ball must hit it twice to break
        if color == WHITE:
            self.health = 200
        else:
            self.health = 100

        # The rect variable is used to handle the placement
        # and the collisions of the object
        self.blockRect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        self.block = pygame.draw.rect(screen, self.color,self.blockRect)

    # Used to render the object on the screen if and only
    # if its health is greater than 0
    def display(self):
        if self.health > 0:
            self.brick = pygame.draw.rect(screen,self.color, self.blockRect)

    # Used to decrease the health of the block
    def hit(self):
        self.health -= self.damage

    # Used to get the rect of the object
    def getRect(self):
        return self.blockRect

    # Used to get the health of the object
    def getHealth(self):
        return self.health


# Ball Class
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac, self.yFac = 1, 1

        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx,self.posy), self.radius)

    # Used to display the object on the screen
    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx,self.posy), self.radius)

    # Used to update the state of the object
    def update(self):
        self.posx += self.xFac*self.speed
        self.posy += self.yFac*self.speed

        # Reflecting the ball if it touches
        # either of the vertical edges
        if self.posx <= 0 or self.posx >= WIDTH:
            self.xFac *= -1

        # Reflection from the top most edge of the screen
        if self.posy <= 0:
            self.yFac *= -1

        # If the ball touches the bottom most edge of
        # the screen, True value is returned
        if self.posy >= HEIGHT:
            return True

        return False

    # Resets the position of the ball
    def reset(self):
        self.posx = 0
        self.posy = HEIGHT
        self.xFac, self.yFac = 1, -1

    # Used to change the direction along Y axis
    def hit(self):
        self.yFac *= -1

    # Returns the rect of the ball. In this case,
    # it is the ball itself
    def getRect(self):
        return self.ball

# Helper Functions

# Function used to check collisions between any two entities


def collisionChecker(rect, ball):
    if pygame.Rect.colliderect(rect, ball):
        return True

    return False


# Function used to populate the blocks
def populateBlocks(blockWidth, blockHeight,horizontalGap, verticalGap):
    listOfBlocks = []

    for i in range(0, WIDTH, blockWidth+horizontalGap):
        for j in range(0, HEIGHT//2, blockHeight+verticalGap):
            listOfBlocks.append(Block(i, j, blockWidth, blockHeight,random.choice([BLUE, GREEN , WHITE])))

    return listOfBlocks

# Once all the lives are over, this function waits until
# exit or space bar is pressed and does the corresponding action
def gameOver():
    gameOver = True

    while gameOver:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

def you_won_screen():
    you_won_message = "You Won!"
    you_won_font = pygame.font.Font('freesansbold.ttf', 50)
    you_won_text = you_won_font.render(you_won_message, True, WHITE)
    you_won_rect = you_won_text.get_rect()
    you_won_rect.center = (WIDTH // 2, HEIGHT // 2)

    restart_font = pygame.font.Font('freesansbold.ttf', 30)
    restart_text = restart_font.render("Press Enter or Space to Play Again", True, WHITE)
    restart_rect = restart_text.get_rect()
    restart_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)

    quit_text = restart_font.render("Press escape to Quit", True, WHITE)
    quit_rect = quit_text.get_rect()
    quit_rect.center = (WIDTH // 2, HEIGHT // 2 + 100)

    screen.fill(BLACK)
    screen.blit(you_won_text, you_won_rect)
    screen.blit(restart_text, restart_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
# Game Over Screen
def game_over_screen():

    game_over_font = pygame.font.Font('freesansbold.ttf', 50)
    game_over_text = game_over_font.render("Game Over!", True, WHITE)
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (WIDTH // 2, HEIGHT // 2)

    restart_font = pygame.font.Font('freesansbold.ttf', 30)
    restart_text = restart_font.render("Press Enter or Space to Play Again", True, WHITE)
    restart_rect = restart_text.get_rect()
    restart_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)

    quit_text = restart_font.render("Press escape to Quit", True, WHITE)
    quit_rect = quit_text.get_rect()
    quit_rect.center = (WIDTH // 2, HEIGHT // 2 + 100)

    screen.fill(BLACK)
    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

# ... (existing main function with modifications)
def main(screen):
    running = True
    lives = 1
    score = 0

    scoreText = font.render("score", True, WHITE)
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.center = (20, HEIGHT-10)

    livesText = font.render("Lives" + str(lives), True, WHITE)
    livesTextRect = livesText.get_rect()
    livesTextRect.center = (120, HEIGHT-10)

    striker = Striker(0, HEIGHT-50, 100, 20, 10, WHITE)
    strikerXFac = 0

    ball = Ball(0, HEIGHT-150, 7, 5, WHITE)

    blockWidth, blockHeight = 40, 15
    horizontalGap, verticalGap = 20, 20

    listOfBlocks = populateBlocks(
        blockWidth, blockHeight, horizontalGap, verticalGap)

    # Game loop
    while running:
        screen.blit(background_image, (0, 0))
        screen.fill(BLACK)
        screen.blit(scoreText, scoreTextRect)
        screen.blit(livesText, livesTextRect)

        scoreText = font.render("Score : " + str(score), True, WHITE)
        livesText = font.render("Lives : " + str(lives), True, WHITE)

        # If all the blocks are destroyed, then we repopulate them
        if not listOfBlocks:
            running = you_won_screen()

        # All the lives are over. So, the gameOver() function is called
        if lives <= 0:
            running = game_over_screen()

            while listOfBlocks:
                listOfBlocks.pop(0)

            lives = 1
            score = 0
            listOfBlocks = populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    strikerXFac = -1
                if event.key == pygame.K_RIGHT:
                    strikerXFac = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    strikerXFac = 0

        # Collision check
        if(collisionChecker(striker.getRect(),ball.getRect())):
            ball.hit()
            collision_sound.play()
        for block in listOfBlocks:
            if(collisionChecker(block.getRect(), ball.getRect())):
                ball.hit()
                block.hit()
                block_hit_sound.play()
                if block.getHealth() <= 0:
                    listOfBlocks.pop(listOfBlocks.index(block))
                    score += 5

        # Update
        striker.update(strikerXFac)
        lifeLost = ball.update()

        if lifeLost:
            lives -= 1
            ball.reset()
            print(lives )

        # Display
        striker.display()
        ball.display()

        for block in listOfBlocks:
            block.display()

        pygame.display.update()
        clock.tick(FPS)


# Game Manager

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Block Breaker")
    clock = pygame.time.Clock()
    background_music.play(loops=-1)  # Start playing background music

    background_image = pygame.image.load('space.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    game_menu(screen, background_music, main)  # Show the game menu

    pygame.quit()