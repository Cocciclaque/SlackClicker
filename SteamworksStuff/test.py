import pygame
from steamworks import STEAMWORKS

# Initialize pygame window (even if it's just a dummy window)
pygame.init()
screen = pygame.display.set_mode((1, 1))  # Create a tiny 1x1 window

# Initialize Steamworks with the correct App ID (Spacewar's App ID is 480)
steamworks = STEAMWORKS()
if steamworks.initialize():
    print("Steamworks is initialized.")
else:
    print("Failed to initialize Steamworks API.")
    pygame.quit()
    exit()  # Exit if Steamworks API failed to initialize

# Get the number of achievements
num_achievements = steamworks.GetNumAchievements()
print(f"Number of achievements: {num_achievements}")

# Loop through all achievements and unlock them
for i in range(num_achievements):
    achievement_name = steamworks.GetAchievementName(i)  # Get the achievement name by index
    is_unlocked = steamworks.GetAchievement(achievement_name)  # Check if already unlocked

    if is_unlocked:
        print(f"Achievement '{achievement_name}' is already unlocked.")
    else:
        if steamworks.SetAchievement(achievement_name):
            print(f"Achievement '{achievement_name}' unlocked successfully!")
            steamworks.StoreStats()  # Store stats after unlocking achievement
        else:
            print(f"Failed to unlock achievement '{achievement_name}'.")

# Main loop to keep the window open until Escape is pressed
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Close the window (optional)
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Press Escape to exit
                running = False

# Quit pygame and Steamworks
pygame.quit()
