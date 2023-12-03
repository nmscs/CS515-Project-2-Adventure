import json
import sys
import random

class TextAdventure:
    def __init__(self, map_file):
        self.load_map(map_file)
        self.current_room = 0
        self.inventory = []
        self.health = 100  # Initial health

    def load_map(self, map_file):
        with open(map_file, 'r') as file:
            self.rooms = json.load(file)

    def save_game(self, save_file):
        game_state = {
            'current_room': self.current_room,
            'inventory': self.inventory,
            'health': self.health
        }
        with open(save_file, 'w') as file:
            json.dump(game_state, file)

    def load_game(self, save_file):
        with open(save_file, 'r') as file:
            game_state = json.load(file)
        self.current_room = game_state['current_room']
        self.inventory = game_state['inventory']
        self.health = game_state.get('health', 100)

    def show_status(self):
        print(f"Health: {self.health}%")

    def handle_random_event(self):
        room = self.rooms[self.current_room]
        if 'events' in room:
            event = random.choice(room['events'])
            print(f"Random Event: {event}")
            # Implement logic for the event

    def show_room(self, room_id):
        room = self.rooms[room_id]
        print(f">{room['name']}\n\n{room['desc']}\n")
        if 'items' in room:
            print(f"Items: {', '.join(room['items'])}")
        print(f"Exits: {', '.join(room['exits'])}\n")

    def play(self):
        while True:
            self.show_status()
            self.show_room(self.current_room)
            self.handle_random_event()
            command = input("What would you like to do? ").strip().lower().split()

            if not command:
                print("Sorry, you need to specify a command.")
                continue

            verb = command[0]
            target = command[1] if len(command) > 1 else None

            if verb in self.match_verb(verb):
                if verb == 'go':
                    self.go(target)
                elif verb == 'look':
                    self.show_room(self.current_room)
                elif verb == 'get':
                    self.get(target)
                elif verb == 'inventory':
                    self.show_inventory()
                elif verb == 'quit':
                    print("Goodbye!")
                    sys.exit()
                elif verb == 'help':
                    self.help()
                elif verb == 'drop':
                    self.drop(target)
                elif verb == 'trade':
                    self.trade(command[1], command[3])
                elif verb == 'direction':
                    self.direction_as_verb(target)
                # Add more verb handlers
            else:
                print(f"Invalid command. Type 'help' for a list of commands.")

    def go(self, direction):
        room = self.rooms[self.current_room]
        if direction in room['exits']:
            self.current_room = room['exits'][direction]
            print(f"You go {direction}.\n")
        else:
            print(f"There's no way to go {direction}.\n")

    def get(self, item):
        room = self.rooms[self.current_room]
        if 'items' in room and item in room['items']:
            self.inventory.append(item)
            room['items'].remove(item)
            print(f"You pick up the {item}.\n")
        else:
            print(f"There's no {item} anywhere.\n")

    def show_inventory(self):
        if not self.inventory:
            print("You're not carrying anything.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"  {item}")
        print()

    def match_verb(self, partial_input):
        valid_verbs = ['go', 'get', 'look', 'inventory', 'quit', 'help', 'drop', 'trade', 'direction']
        matches = [verb for verb in valid_verbs if verb.startswith(partial_input)]
        return matches

    def help(self):
        valid_verbs = self.match_verb('')
        print("You can run the following commands:")
        for verb in valid_verbs:
            print(f"  {verb} ...")

    def drop(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            room = self.rooms[self.current_room]
            room['items'].append(item)
            print(f"You drop the {item}.\n")
        else:
            print(f"You don't have {item} in your inventory.\n")

    def direction_as_verb(self, direction):
        matches = self.match_direction(direction)
        if len(matches) == 1:
            self.go(matches[0])
        elif len(matches) > 1:
            print(f"Did you mean {', '.join(matches)}?")
        else:
            print(f"There's no way to go {direction}.\n")

    def match_direction(self, partial_input):
        room = self.rooms[self.current_room]
        valid_directions = list(room['exits'])  # Include full exit names
        valid_directions.extend([d[:len(partial_input)] for d in room['exits']])  # Include abbreviations
        matches = [direction for direction in valid_directions if direction.startswith(partial_input)]
        return matches

    def match_item(self, partial_input):
        room = self.rooms[self.current_room]
        if 'items' in room:
            matches = [item for item in room['items'] if item.startswith(partial_input)]
            return matches
        return []

    def trade(self, item_to_give, item_to_receive):
        if item_to_give in self.inventory:
            self.inventory.remove(item_to_give)
            self.inventory.append(item_to_receive)
            print(f"You trade the {item_to_give} for {item_to_receive}.\n")
        else:
            print(f"You don't have {item_to_give} to trade.\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py Adventure.json")
        sys.exit(1)

    game = TextAdventure(sys.argv[1])
    game.play()
