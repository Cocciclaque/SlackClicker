from steamworks import STEAMWORKS

steamworks = STEAMWORKS()
if steamworks.initialize():
    print("Steamworks is initialized.")
else:
    print("Failed to initialize Steamworks API.")
    exit() 


def getAchievement(name:str) -> None:

    is_unlocked = steamworks.GetAchievement(name)  # Check if already unlocked

    if is_unlocked:
        print(f"Achievement '{name}' is already unlocked.")
    else:
        if steamworks.SetAchievement(name):
            print(f"Achievement '{name}' unlocked successfully!")
            steamworks.StoreStats()  # Store stats after unlocking achievement
        else:
            print(f"Failed to unlock achievement '{name}'.")

getAchievement(b'BEGINNING_0')