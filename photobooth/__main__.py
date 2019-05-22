import pygame

#initialize pygame instance
pygame.init()
screen = pygame.display.set_mode((800, 600))

running = True

def WaitForUser():
    global pygame
    global running

    # Keep running loop until we find a key press
    FoundKeyPress = False
    while not FoundKeyPress:

        # Wait for input from the user
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                # Close out of the application on <ESC>
                if event.key == pygame.K_ESCAPE:
                    FoundKeyPress = True
                    running = False

                # Trigger the found key press so the application can continue
                if event.key == pygame.K_DOWN:
                    FoundKeyPress = True

            # Userf closed out of app with 'X' button in top left
            if event.type == pygame.QUIT:
                FoundKeyPress = True
                running = False



# Keep the application running
while running:
    WaitForUser()

