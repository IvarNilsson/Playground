import pygame
import math

# Initialize pygame
pygame.init()

# Screen dimensions and scale factor
scale = 0.5
SCREEN_WIDTH, SCREEN_HEIGHT = int(2000 * scale), int(1800 * scale)
MAP_HEIGHT = int(1500 * scale)

# Set up the screen and window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Guess the Location Game")

# Load the map image
map_image = pygame.image.load("map.png")

scaled_map_width = int(2000 * scale)  # Scale map width
scaled_map_height = int(1500 * scale)  # Scale map height

map_image = pygame.transform.scale(map_image, (scaled_map_width, scaled_map_height))

# Now map_image is scaled and you can draw it directly on the screen
screen.blit(map_image, (0, 0))  # Draw the scaled map

map_rect = map_image.get_rect()

map_rect = pygame.Rect(0, 0, SCREEN_WIDTH, MAP_HEIGHT)

# Game loop
running = True

player_click_pos = None  # Store the player's click position (initially None)

while running:
    screen.fill((255, 255, 255))  # Fill the screen with white
    screen.blit(map_image, (0, 0))  # Draw the map

    # Draw the bottom area (300 pixels high)
    pygame.draw.rect(screen, (200, 200, 200), (0, SCREEN_HEIGHT - int(300 * scale), SCREEN_WIDTH, int(300 * scale)))

    # Draw the green dot where the player clicks (only if not locked in)
    if player_click_pos:
        pygame.draw.circle(screen, (0, 255, 0), player_click_pos, int(10 * scale))  # Green dot (scaled)
 
    # Draw the buttons
    mouse_pos = pygame.mouse.get_pos()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if map_rect.collidepoint(mouse_pos):
                    # Store the clicked position
                    player_click_pos = pygame.mouse.get_pos()
                    print(player_click_pos) 

    pygame.display.flip()  # Update the display

pygame.quit()
