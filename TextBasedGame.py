# TextBasedGame.py
# Kieran (James) Reeves
# A text adventure game set aboard the haunted SS Elysium
# Goal: Collect all 6 shards before confronting Captain Varnholt

import random

def show_instructions():
    """Display game introduction and available commands."""
    print("\n" + "="*50)
    print("  SS Elysium: Heart of the Deep")
    print("="*50)
    print("You woke up aboard the derelict SS Elysium.")
    print("Collect all 6 shards to defeat Captain Varnholt.")
    print("If you reach his quarters without all shards, he claims your soul.")
    print("\nCommands:")
    print("  n / north / e / east / s / south / w / west   → move")
    print("  take <item> / get <item>                       → pick up item")
    print("  use <item>                                     → use special item")
    print("  look                                           → redisplay room")
    print("  i / inventory                                  → show inventory")
    print("  help                                           → show this help")
    print("  quit                                           → exit game")
    print("="*50 + "\n")


def show_status(current_room, inventory, shard_inventory, rooms):
    """Display current room description, visible items, exits, and status."""
    room = rooms[current_room]
    has_light = "Lantern" in inventory or not room["dark"]

    print(f"\n[{current_room}]")
    print(room["desc"])

    # Show visible items
    visible = []
    if has_light:
        if room.get("item") and room["item"] not in shard_inventory:
            visible.append(room["item"])
        if room.get("utility") and room["utility"] not in inventory:
            visible.append(room["utility"])

    if visible:
        print("You see:", ", ".join(visible))
    else:
        if not has_light:
            print("It's pitch black. You can barely see your hand in front of your face.")

    # Show available exits (hide locked doors unless key is held)
    exits_list = []
    for direction, dest in room["exits"].items():
        if rooms[dest].get("locked", False) and "Rusty Key" not in inventory:
            continue
        exits_list.append(f"{direction.upper()}: {dest}")

    if exits_list:
        print("Exits:", ", ".join(exits_list))
    else:
        print("Exits: None")

    # Status line
    print(f"Shards collected: {len(shard_inventory)}/6")
    inv_str = ", ".join(inventory) if inventory else "empty"
    print(f"Inventory: {inv_str}\n")


def main():
    # ────────────────────────────────────────────────
    # Game data - Rooms
    # ────────────────────────────────────────────────
    rooms = {
        "Grand Foyer": {
            "desc": "Opulent entry hall with dusty chandeliers and faded grandeur. The ship groans to life around you. (START)",
            "item": None,
            "utility": None,
            "locked": False,
            "dark": False,
            "exits": {
                "west": "Library",
                "east": "Radio Room",
                "south": "Dining Room"
            }
        },
        "Library": {
            "desc": "Shelves of moldy books line the walls; a flickering lantern casts eerie shadows. You see a glint in a dusty corner.",
            "item": "Sapphire Shard",
            "utility": "Lantern",
            "locked": False,
            "dark": False,
            "exits": {
                "east": "Grand Foyer",
                "south": "Great Ballroom"
            }
        },
        "Radio Room": {
            "desc": "Crackling static from the old radio equipment haunts the foggy room. A faded log on the desk reads: 'Shards of six may bind the soul.'",
            "item": None,
            "utility": None,
            "locked": False,
            "dark": False,
            "exits": {
                "south": "Cargo",
                "west": "Grand Foyer"
            }
        },
        "Cargo": {
            "desc": "Crates of forgotten luggage and supplies are stacked high, though many have tipped over. A dim light through a porthole gleams off a key hanging on the wall.",
            "item": "Rusty Key",
            "utility": None,
            "locked": False,
            "dark": False,
            "exits": {
                "north": "Radio Room"
            }
        },
        "Dining Room": {
            "desc": "Long tables set with shattered dishes; lace tablecloths turn to dust on contact. A pearl centerpiece steals the show, unaffected by time. Ghostly whispers echo from beyond.",
            "item": "Pearl Shard",
            "utility": None,
            "locked": False,
            "dark": False,
            "exits": {
                "north": "Grand Foyer",
                "south": "Great Ballroom"
            }
        },
        "Great Ballroom": {
            "desc": "Mirror shine on the dance floor marred by a dark fissure. A massive chandelier with an emerald inlay lies smashed into the ground.",
            "item": "Emerald Shard",
            "utility": None,
            "locked": False,
            "dark": False,
            "exits": {
                "north": "Dining Room",
                "east": "Infirmary",
                "south": "Pool Deck",
                "west": "Library"
            }
        },
        "Pool Deck": {
            "desc": "A nearly empty pool; putrid water in the deep end gives off an eerie blue glow. Items long ago turned into a coral system.",
            "item": "Coral Shard",
            "utility": None,
            "locked": False,
            "dark": False,
            "exits": {
                "north": "Great Ballroom",
                "east": "Infirmary",
                "south": "Engine Room"
            }
        },
        "Infirmary": {
            "desc": "Rusted wheelchairs roll back and forth with the swells. A glass medicine cabinet on the rear wall holds a gold glimmer.",
            "item": "Gold Shard",
            "utility": None,
            "locked": False,
            "dark": False,
            "exits": {
                "west": "Great Ballroom"
            }
        },
        "Engine Room": {
            "desc": "Massive grinding gears and boiling pipes fill the humid air. Metal clangs loudly in the pitch black dark. (Requires key + lantern)",
            "item": "Obsidian Shard",
            "utility": None,
            "locked": True,
            "dark": True,
            "exits": {
                "north": "Pool Deck",
                "east": "Captain’s Quarters"
            }
        },
        "Captain’s Quarters": {
            "desc": "The captain’s dark cabin pulses with malevolent energy. Captain Elias Varnholt awaits you, eyes glowing green. There is no escape.",
            "item": None,
            "utility": None,
            "locked": False,
            "dark": False,
            "exits": {
                "west": "Engine Room"
            }
        }
    }

    # ────────────────────────────────────────────────
    # Game state variables
    # ────────────────────────────────────────────────
    current_room = "Grand Foyer"
    inventory = []
    shard_inventory = []
    shard_list = ["Sapphire Shard", "Pearl Shard", "Emerald Shard",
                  "Coral Shard", "Obsidian Shard", "Gold Shard"]
    TOTAL_SHARDS = 6
    game_over = False

    ghost_events = [
        "Captain whispers: 'You’ll join my crew soon…'",
        "Shadows coil around your legs — you’re suddenly back in the Grand Foyer!",
        "Icy fog chills your bones… nothing happens this time.",
        "A child’s laughter echoes behind you… but no one is there."
    ]

    show_instructions()

    # ────────────────────────────────────────────────
    # Main game loop
    # ────────────────────────────────────────────────
    while not game_over:
        # Random ghost event (~10% chance)
        if random.randint(1, 100) <= 10:
            event = random.choice(ghost_events)
            print("\n" + event)
            if "Foyer" in event:
                current_room = "Grand Foyer"
            print("-" * 40)
            continue

        # Show room & status
        show_status(current_room, inventory, shard_inventory, rooms)

        # Get player input
        command = input("> ").strip().lower()
        if not command:
            continue

        words = command.split()
        verb = words[0]
        arg = " ".join(words[1:]) if len(words) > 1 else ""

        # ── Movement ─────────────────────────────────────
        if verb in ["n", "north", "e", "east", "s", "south", "w", "west"]:
            dir_map = {"n": "north", "e": "east", "s": "south", "w": "west"}
            direction = dir_map.get(verb, verb)

            if direction in rooms[current_room]["exits"]:
                next_room = rooms[current_room]["exits"][direction]

                # Check if destination is locked
                if rooms[next_room].get("locked", False) and "Rusty Key" not in inventory:
                    print("The door is locked. You need a key.")
                else:
                    current_room = next_room

                    # Check win/lose condition
                    if current_room == "Captain’s Quarters":
                        if len(shard_inventory) == TOTAL_SHARDS:
                            print("\n" + "="*60)
                            print("The six shards unite into a blazing heart of light!")
                            print("Captain Varnholt screams as his form dissolves.")
                            print("The SS Elysium begins to calm… You have broken the curse.")
                            print("*** YOU WIN! ***")
                        else:
                            print("\n" + "="*60)
                            print("Captain Elias Varnholt smiles with rotting teeth.")
                            print("'Welcome to the crew… forever.'")
                            print("*** YOU LOSE ***")
                        game_over = True
            else:
                print("You can't go that way.")

        # ── Take / Get item ──────────────────────────────
        elif verb in ["take", "get"] and arg:
            room = rooms[current_room]
            has_light = "Lantern" in inventory or not room["dark"]  # Note: This works post-fix (title case in inv)

            if not has_light:
                print("It's too dark to see anything clearly.")
            elif room.get("item") and arg == room["item"].lower():
                original_item = room["item"]
                inventory.append(original_item)
                if original_item in shard_list:
                    shard_inventory.append(original_item)
                room["item"] = None
                print(f"You take the {original_item}.")
            elif room.get("utility") and arg == room["utility"].lower():
                original_item = room["utility"]
                inventory.append(original_item)
                room["utility"] = None
                print(f"You take the {original_item}.")
            else:
                print("No such item here.")

        # ── Use item ─────────────────────────────────────
        elif verb == "use" and arg and arg in inventory:
            if arg == "Rusty Key" and current_room == "Great Ballroom" and rooms["Engine Room"]["locked"]:
                # Using key anywhere near Engine Room entrance (simplified)
                rooms["Engine Room"]["locked"] = False
                print("You unlock the heavy door to the Engine Room.")
            elif arg == "Lantern" and rooms[current_room]["dark"]:
                print("You light the lantern. The darkness retreats — you can see clearly now.")
            else:
                print(f"You can't use {arg} here (or it has no effect).")

        # ── Other commands ───────────────────────────────
        elif verb == "look":
            print(rooms[current_room]["desc"])

        elif verb in ["i", "inventory"]:
            print("Inventory:", ", ".join(inventory) or "empty")
            print("Shards:", ", ".join(shard_inventory) or "none")

        elif verb == "help":
            show_instructions()

        elif verb == "quit":
            print("Goodbye.")
            game_over = True

        else:
            print("Unknown command. Type 'help' for commands.")

        print("-" * 40)

    print("\nGAME OVER.\n")


if __name__ == "__main__":
    main()