import pygame
import random

pygame.init()

player_score = 0
bot_score = 0
ball_speed_x = 5 * random.choice((1, -1)) 
ball_speed_y = 5 * random.choice((1, -1))

punk = pygame.mixer.Sound('./music/ball_music.mp3')

def move_wallplayer():
    pygame.mouse.set_visible(False)
    x, y = pygame.mouse.get_pos()
    player.rect.y += (y - player.rect.y) * 0.2
    if player.rect.top < 0:
        player.rect.top = 0
    if player.rect.bottom > SCREEN_HEIGHT:
        player.rect.bottom = SCREEN_HEIGHT

def move_wallbot():
    if bot.rect.centery < ball.rect.centery:
        bot.rect.y += 4
    else:
        bot.rect.y -= 4
    if bot.rect.top < 0:
        bot.rect.top = 0
    if bot.rect.bottom > SCREEN_HEIGHT:
        bot.rect.bottom = SCREEN_HEIGHT

def ball_movement():
    global ball_speed_x, ball_speed_y, player_score, bot_score 
    ball.rect.x += ball_speed_x
    ball.rect.y += ball_speed_y
    

    if ball.rect.top <= 0 or ball.rect.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    if pygame.sprite.collide_mask(ball, player):
        ball.rect.left = player.rect.right
        ball_speed_x *= -1
        ball_speed_y = random.randint(-8, 8)
        punk.play()

    if pygame.sprite.collide_mask(ball, bot):
        ball.rect.right = bot.rect.left
        ball_speed_x *= -1
        ball_speed_y = random.randint(-8, 8)
        punk.play()

    if abs(ball_speed_y) < 2:
        ball_speed_y = 2 * random.choice([-1, 1])

    if ball.rect.left <= 0:
        bot_score += 1
        reset_ball()

    if ball.rect.right >= SCREEN_WIDTH:
        player_score += 1
        reset_ball()

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    ball_speed_x = 5 * random.choice((1, -1))
    ball_speed_y = 5 * random.choice((1, -1))

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
ball = pygame.sprite.Group()
arrow = pygame.sprite.Group()

player = pygame.sprite.Sprite(all_sprites, walls)
player.image = pygame.image.load('./imgs/wallplayer.png')
player.rect = player.image.get_rect()
player.rect.centerx = 15
player.rect.centery = SCREEN_HEIGHT // 2

bot = pygame.sprite.Sprite(all_sprites, walls)
bot.image = pygame.image.load('./imgs/wallbot.png')
bot.rect = player.image.get_rect()
bot.rect.centerx = SCREEN_WIDTH - 15
bot.rect.centery = SCREEN_HEIGHT // 2

ball = pygame.sprite.Sprite(all_sprites, ball)
ball.image = pygame.image.load('./imgs/ball.png')
ball.rect = ball.image.get_rect()

ball.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

run = True
run = True
while run:
    screen.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    move_wallbot()
    ball_movement()
    move_wallplayer()

    font = pygame.font.Font(None, 74)
    
    text_player = font.render(str(player_score), True, (0, 0, 255))
    text_rect_player = text_player.get_rect(center=(SCREEN_WIDTH//2 - 50, 30))
    screen.blit(text_player, text_rect_player)
    
    text_bot = font.render(str(bot_score), True, (255, 0, 0))
    text_rect_bot = text_bot.get_rect(center=(SCREEN_WIDTH//2 + 50, 30))
    screen.blit(text_bot, text_rect_bot)
    
    colon_text = font.render(":", True, (255, 255, 255))
    colon_rect = colon_text.get_rect(center=(SCREEN_WIDTH//2, 30))
    screen.blit(colon_text, colon_rect)

    all_sprites.draw(screen)
    pygame.display.update()
    clock.tick(90)

pygame.quit()