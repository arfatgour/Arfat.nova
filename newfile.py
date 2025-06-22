import pygame
import random

pygame.init()

# Screen setup
width, height = 360, 640
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
block = 20
speed = 10

font = pygame.font.SysFont("Arial", 26)

def draw_text(text, pos, color=(255, 255, 255)):
    label = font.render(text, True, color)
    win.blit(label, pos)

def draw_button(rect, label):
    pygame.draw.rect(win, (0, 255, 0), rect, border_radius=8)
    draw_text(label, (rect.x + 18, rect.y + 5), (0, 0, 0))

def game_loop():
    x = width // 2
    y = height // 2
    dx = 0
    dy = 0
    started = False

    snake = [(x, y)]
    food = (random.randrange(0, width, block), random.randrange(0, height - 120, block))
    score = 0

    # Bigger center control buttons
    btn_size = 60
    center_x = width // 2
    center_y = height - 80
    btn_up = pygame.Rect(center_x - btn_size // 2, center_y - btn_size - 10, btn_size, btn_size)
    btn_down = pygame.Rect(center_x - btn_size // 2, center_y + btn_size + 10 - btn_size, btn_size, btn_size)
    btn_left = pygame.Rect(center_x - btn_size - 10, center_y, btn_size, btn_size)
    btn_right = pygame.Rect(center_x + 10, center_y, btn_size, btn_size)

    running = True
    while running:
        win.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if btn_up.collidepoint(mx, my) and dy == 0:
                    dx, dy = 0, -block
                    started = True
                elif btn_down.collidepoint(mx, my) and dy == 0:
                    dx, dy = 0, block
                    started = True
                elif btn_left.collidepoint(mx, my) and dx == 0:
                    dx, dy = -block, 0
                    started = True
                elif btn_right.collidepoint(mx, my) and dx == 0:
                    dx, dy = block, 0
                    started = True

        if started:
            x += dx
            y += dy

        # Wrap-around screen edges
        x %= width
        y %= (height - 100)  # Leave space for buttons

        if started and (x, y) in snake:
            draw_text("Game Over", (100, 280), (255, 0, 0))
            pygame.display.update()
            pygame.time.wait(2000)
            return

        if started:
            snake.append((x, y))
            if (x, y) == food:
                score += 1
                food = (random.randrange(0, width, block), random.randrange(0, height - 120, block))
            else:
                snake.pop(0)

        pygame.draw.rect(win, (255, 0, 0), (*food, block, block))
        for pos in snake:
            pygame.draw.rect(win, (0, 255, 0), (*pos, block, block))

        draw_text(f"Score: {score}", (10, height - 90))

        # Buttons
        draw_button(btn_up, "↑")
        draw_button(btn_down, "↓")
        draw_button(btn_left, "←")
        draw_button(btn_right, "→")

        pygame.display.update()
        clock.tick(speed)

    pygame.quit()

game_loop()