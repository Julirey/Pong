import pygame, sys, random

def ball_animation():
    """
    Activates ball movement, collision, bounce, and scoring logic
    """ 
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Display border collision bounce
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    # Ball touches the left border | Player Score
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        player_score += 1

    # Ball touches the right border | Opponent Score
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        opponent_score += 1

    # Ball to Player Paddle collision
    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    # Ball to Opponent Paddle collision
    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1


def player_animation():
    """
    Enables player movement and collision 
    """ 
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_ai():
    """
    Activates opponent ai and collision 
    """ 
    if opponent.top < ball.y:
        opponent.y += opponent_speed
    if opponent.bottom > ball.y:
        opponent.y -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_start():
    """
    Prevents ball from moving before the counter ends and resets the ball if called after the end of the countdown.
    """ 
    global ball_speed_x, ball_speed_y, ball_moving, score_time

    ball.center = (screen_width / 2, screen_height / 2)
    current_time = pygame.time.get_ticks()

    if current_time - score_time < 700:
        number_three = score_font.render("3", False, white)
        screen.blit(number_three, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = score_font.render("2", False, white)
        screen.blit(number_two, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = score_font.render("1", False, white)
        screen.blit(number_one, (screen_width / 2 - 10, screen_height / 2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x = 0
        ball_speed_y = 0
        
    else:
        ball_speed_x = 7 * random.choice((1, -1))
        ball_speed_y = 7 * random.choice((1, -1))
        score_time = None


# PyGame Setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Colors
white = (255, 255, 255)
bg_color = pygame.Color("black")

# Game Models
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)

paddle_width = 20
paddle_height = 120
player = pygame.Rect(screen_width - 30, screen_height / 2 - (paddle_height / 2), paddle_width, paddle_height)
opponent = pygame.Rect(10, screen_height / 2 - (paddle_height / 2), paddle_width, paddle_height)

# Game Variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
player_velocity = 10
opponent_speed = 10
ball_moving = False
score_time = True

# Score Text
player_score = 0
opponent_score = 0
score_font = pygame.font.SysFont("impact", 40)

# SFX
pong_sound = pygame.mixer.Sound("sfx/pong.ogg")
score_sound = pygame.mixer.Sound("sfx/score.ogg")

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Keyboard movement | w/s up/down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w :
                player_speed -= player_velocity
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_speed += player_velocity
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w :
                player_speed += player_velocity
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_speed -= player_velocity

    # Game Physics
    ball_animation()
    player_animation()
    opponent_ai()

    # Graphics
    screen.fill(bg_color)
    pygame.draw.rect(screen, white, player)
    pygame.draw.rect(screen, white, opponent)
    pygame.draw.ellipse(screen, white, ball)

    if score_time:
        ball_start()

    # Score renders
    player_text = score_font.render(f"{player_score}", False, white)
    screen.blit(player_text, (screen_width / 2 + 20, 50))

    opponent_text = score_font.render(f"{opponent_score}", False, white)
    screen.blit(opponent_text, (screen_width / 2 - 40 , 50))

    pygame.display.update()
    clock.tick(60)
