# ModuleSixMilestone.py
# Name: Kieran (James) Reeves
# SNHU CS-110 / IT-140 - Module Six Milestone
# Simplified text-based adventure game focusing on room movement using a dictionary
# Date: February 15, 2026

# Dictionary linking rooms to possible moves
# Keys are current room names, values are dictionaries of direction → next room
rooms = {
    'Great Hall': {'South': 'Bedroom'},
    'Bedroom': {'North': 'Great Hall', 'East': 'Cellar'},
    'Cellar': {'West': 'Bedroom'}
}

# Starting room
current_room = 'Great Hall'

# Main gameplay loop
while current_room != 'exit':
    # Display current location
    print(f"\nYou are in the {current_room}.")

    # Show possible exits
    if current_room in rooms and rooms[current_room]:
        possible_directions = list(rooms[current_room].keys())
        print(f"Possible directions: {', '.join(possible_directions)}")
    else:
        print("No exits from here.")

    # Get player input
    command = input("\nWhat would you like to do? ").strip().lower()

    # Handle the command
    if command == 'exit':
        print("Thanks for playing! Goodbye.")
        current_room = 'exit'  # This will end the loop
    elif command.startswith('go '):
        # Extract the direction (e.g., "go north" → "north")
        direction = command[3:].strip().capitalize()

        # Check if the direction is valid from current room
        if current_room in rooms and direction in rooms[current_room]:
            # Move to the new room
            current_room = rooms[current_room][direction]
            print(f"Moving {direction.lower()} to the {current_room}...")
        else:
            # Invalid direction or no exit that way
            print(f"You can't go {direction.lower()} from here!")
    else:
        # Any other input is invalid
        print("Invalid command. Try 'go North', 'go South', 'go East', 'go West', or 'exit'.")

# Game has ended (player chose exit)
print("\nGame over.")