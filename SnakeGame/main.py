import pygame
import time
import random

pygame.init()

dis_width = 720
dis_height = 480

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

snake_block = 10
snake_speed = 15

dis = pygame.display.set_mode((dis_width, dis_height))

pygame.display.set_caption('Snake Game using PyGame')

clock = pygame.time.Clock()

snake_pos = [100, 50]

snake_body = [[100, 50]]

food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


def spawnFood():
    return [random.randrange(1, (dis_width // 10)) * 10,
            random.randrange(3, (dis_height // 10)) * 10]


food_pos = spawnFood()


def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    dis.blit(score_surface, score_rect)


def game_Over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (dis_width / 2, dis_height / 4)

    dis.blit(game_over_surface, game_over_rect)
    pygame.display.update()

    time.sleep(2)
    pygame.quit()
    quit()


def spawnEntities():
    dis.fill(green)
    for pos in snake_body:
        pygame.draw.rect(dis, blue, pygame.Rect(pos[0], pos[1], snake_block, snake_block))
    pygame.draw.rect(dis, red, pygame.Rect(food_pos[0], food_pos[1], snake_block, snake_block))


def CallForGameOver():
    if snake_pos[0] < 0 or snake_pos[0] > dis_width - 10:
        game_Over()
    # print("Game OVer")

    if snake_pos[1] < 0 or snake_pos[1] > dis_height - 10:
        game_Over()
    # print("GameOver")

    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_Over()


def food_increment():
    global score, food_spawn, food_pos
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 10
        food_spawn = False
    else:
        snake_body.pop()
    if not food_spawn:
        food_pos = spawnFood()
    food_spawn = True


def main():
    global change_to, direction, score, food_spawn
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_Over()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        food_increment()
        spawnEntities()
        CallForGameOver()
        show_score(black, 'times new roman', 20)

        pygame.display.update()
        clock.tick(snake_speed)


if __name__ == '__main__':
    main()
