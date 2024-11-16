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


# Host's points (coordinates with floor numbers)
points = [
    (int(400 * scale), int(300 * scale), 1),
    (int(1000 * scale), int(300 * scale), 2),
    (int(400 * scale), int(900 * scale), 3),
    (int(600 * scale), int(300 * scale), -1),
    (int(400 * scale), int(600 * scale), 3),
    (int(800 * scale), int(300 * scale), 1)
]

# Font for displaying text (scaled)
font = pygame.font.SysFont('Arial', int(32 * scale))  # Scale font size

# Button sizes and positions (scaled)
BUTTON_COLOR = (0, 128, 0)
HOVER_COLOR = (0, 255, 0)
BUTTON_WIDTH, BUTTON_HEIGHT = int(200 * scale), int(50 * scale)

map_rect = pygame.Rect(0, 0, SCREEN_WIDTH, MAP_HEIGHT)
button_up_rect = pygame.Rect(SCREEN_WIDTH // 4 - BUTTON_WIDTH // 2, SCREEN_HEIGHT - int(100 * scale), BUTTON_WIDTH, BUTTON_HEIGHT)
button_down_rect = pygame.Rect(SCREEN_WIDTH * 3 // 4 - BUTTON_WIDTH // 2, SCREEN_HEIGHT - int(100 * scale), BUTTON_WIDTH, BUTTON_HEIGHT)
lock_in_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT - int(200 * scale), BUTTON_WIDTH, BUTTON_HEIGHT)
next_round_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT - int(300 * scale), BUTTON_WIDTH, BUTTON_HEIGHT)

# Function to calculate distance
def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) / scale

# Function to display text on the screen (scaled)
def display_message(text, color, position, font_size=int(32 * scale)):
    font = pygame.font.SysFont('Arial', font_size)
    message = font.render(text, True, color)
    screen.blit(message, position)

# Game loop
running = True
guessed = False
round = 0
distance = 99999
current_floor = 1  # Starting on floor 1
lock_in_pressed = False  # Boolean to track if the Lock In button is pressed
player_click_pos = None  # Store the player's click position (initially None)
wrong_floor_message = False  # Boolean to check if the player clicked on the wrong floor
dot_placed = False  # Track if the player has placed a dot

while running:
    screen.fill((255, 255, 255))  # Fill the screen with white
    screen.blit(map_image, (0, 0))  # Draw the map

    # Draw the host's point (visible or hidden based on your preference)
    pygame.draw.circle(screen, (255, 0, 0), points[round][:2], int(5 * scale))  # Host's point (scaled)

    # Draw the bottom area (300 pixels high)
    pygame.draw.rect(screen, (200, 200, 200), (0, SCREEN_HEIGHT - int(300 * scale), SCREEN_WIDTH, int(300 * scale)))

    # Draw the green dot where the player clicks (only if not locked in)
    if player_click_pos:
        pygame.draw.circle(screen, (0, 255, 0), player_click_pos, int(10 * scale))  # Green dot (scaled)

    # Display the player's guess distance only if Lock In button is pressed
    if guessed and lock_in_pressed:
        # Check if the player clicked on the wrong floor
        if wrong_floor_message:
            display_message("Wrong floor!", (255, 0, 0), (20, SCREEN_HEIGHT - int(280 * scale)))
        else:
            display_message(f"Your guess is {distance:.2f} pixels away!", (0, 0, 0), (20, SCREEN_HEIGHT - int(280 * scale)))

    # Display current floor
    display_message(f"Floor: {current_floor}", (0, 0, 0), (SCREEN_WIDTH // 2 - int(50 * scale), SCREEN_HEIGHT - int(100 * scale)))

    # Display current round
    display_message(f"Round: {round + 1}", (0, 0, 0), (SCREEN_WIDTH // 2 - int(50 * scale), SCREEN_HEIGHT - int(250 * scale)))  # Round starts from 1

    # Draw the buttons
    mouse_pos = pygame.mouse.get_pos()

    if button_up_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, HOVER_COLOR, button_up_rect)  # Button hover effect
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_up_rect)

    if button_down_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, HOVER_COLOR, button_down_rect)  # Button hover effect
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_down_rect)

    if lock_in_button_rect.collidepoint(mouse_pos) and dot_placed:  # Only show Lock In if a dot has been placed
        pygame.draw.rect(screen, HOVER_COLOR, lock_in_button_rect)  # Button hover effect
    elif dot_placed:
        pygame.draw.rect(screen, BUTTON_COLOR, lock_in_button_rect)
        display_message("Lock In", (255, 255, 255), (lock_in_button_rect.x + int(BUTTON_WIDTH // 4), lock_in_button_rect.y + int(10 * scale)))

    if next_round_button_rect.collidepoint(mouse_pos) and lock_in_pressed:  # Only show Next Round after Lock In
        pygame.draw.rect(screen, HOVER_COLOR, next_round_button_rect)  # Button hover effect
    elif lock_in_pressed:
        pygame.draw.rect(screen, BUTTON_COLOR, next_round_button_rect)
        display_message("Next Round", (255, 255, 255), (next_round_button_rect.x + int(BUTTON_WIDTH // 6), next_round_button_rect.y + int(10 * scale)))


    # Display button text
    display_message("Up", (255, 255, 255), (button_up_rect.x + int(BUTTON_WIDTH // 3), button_up_rect.y + int(10 * scale)))
    display_message("Down", (255, 255, 255), (button_down_rect.x + int(BUTTON_WIDTH // 3), button_down_rect.y + int(10 * scale)))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if map_rect.collidepoint(mouse_pos):
                    # Store the clicked position
                    if not lock_in_pressed:
                        player_click_pos = pygame.mouse.get_pos()
                        distance = calculate_distance(player_click_pos, points[round][:2])

                    # Check if the clicked point is on the correct floor
                    if points[round][2] != current_floor:  # If the floor doesn't match
                        wrong_floor_message = True
                    else:
                        wrong_floor_message = False

                    # Set dot_placed to True
                    dot_placed = True
                    guessed = True

                if button_up_rect.collidepoint(mouse_pos):  # "Up" button clicked
                    current_floor += 1  # Increase the floor number

                if button_down_rect.collidepoint(mouse_pos):  # "Down" button clicked
                    current_floor -= 1  # Decrease the floor number

                if lock_in_button_rect.collidepoint(mouse_pos) and dot_placed:  # "Lock In" button clicked
                    lock_in_pressed = True  # Lock in the distance display

                if next_round_button_rect.collidepoint(mouse_pos) and lock_in_pressed:  # "Next Round" button clicked
                    # Increase round number, reset for new round
                    round = (round + 1) % len(points)  # Cycle through points (or add new rounds logic)
                    player_click_pos = None  # Reset player's click position for new round
                    lock_in_pressed = False  # Reset lock-in for next round
                    guessed = False  # Reset guess state
                    wrong_floor_message = False  # Reset wrong floor message
                    dot_placed = False  # Reset dot placement

    pygame.display.flip()  # Update the display

pygame.quit()
