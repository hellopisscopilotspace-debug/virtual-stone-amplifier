import time
import os

class Stone:
    def __init__(self, name, power, ghz):
        self.name = name
        self.power = power
        self.ghz = ghz
        self.history = [(power, ghz)]

    def amplify(self):
        self.power *= 1.25
        self.ghz *= 1.25
        self.history.append((self.power, self.ghz))

    def display_bar(self, max_length=50):
        ratio = min(self.power / 100, 1.0)
        filled = int(ratio * max_length)
        return '[' + '#' * filled + '-' * (max_length - filled) + ']'

class VirtualSpace:
    def __init__(self):
        self.stones = []

    def add_stone(self, stone):
        self.stones.append(stone)
        print(f"Added {stone.name} (Power: {stone.power:.2f}, Virtual GHz: {stone.ghz:.2f})")

    def combine(self, name1, name2):
        s1 = next((s for s in self.stones if s.name == name1), None)
        s2 = next((s for s in self.stones if s.name == name2), None)
        if s1 and s2:
            new_name = f"{s1.name}-{s2.name}"
            new_power = s1.power + s2.power
            new_ghz = s1.ghz + s2.ghz
            new_stone = Stone(new_name, new_power, new_ghz)
            self.add_stone(new_stone)
        else:
            print("Error: Stone(s) not found.")

    def amplify_all(self):
        for s in self.stones:
            s.amplify()

    def status(self):
        print("="*70)
        for s in self.stones:
            print(f"{s.name:20} {s.display_bar()} {s.power:.2f} Power | {s.ghz:.2f} GHz")
        total_power = sum(s.power for s in self.stones)
        total_ghz = sum(s.ghz for s in self.stones)
        efficiency = (total_power / total_ghz * 100) if total_ghz else 0
        print("-"*70)
        print(f"TOTAL POWER: {total_power:.2f}")
        print(f"TOTAL GHz: {total_ghz:.2f}")
        print(f"SYSTEM EFFICIENCY: {efficiency:.2f}%")
        print("="*70)

    def history(self, name):
        s = next((s for s in self.stones if s.name == name), None)
        if s:
            print(f"--- History for {name} ---")
            for idx, (p, g) in enumerate(s.history):
                print(f"Step {idx+1}: Power={p:.2f}, Virtual GHz={g:.2f}")
        else:
            print("Error: Stone not found.")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    vs = VirtualSpace()
    # Initial stones
    vs.add_stone(Stone("Ruby", 10.0, 1.0))
    vs.add_stone(Stone("Sapphire", 15.0, 1.5))
    vs.add_stone(Stone("Emerald", 20.0, 2.0))

    cycle = 1
    while True:
        clear_console()
        print(f"--- Virtual Stone Amplifier | Cycle {cycle} ---\n")
        vs.status()
        print("\nCommands: [amplify NAME] [combine NAME1 NAME2] [history NAME] [exit]")
        command = input("Enter command: ").strip().split()
        if not command:
            continue

        if command[0].lower() == "amplify" and len(command) == 2:
            stone = next((s for s in vs.stones if s.name == command[1]), None)
            if stone:
                stone.amplify()
                print(f"\nAmplified {stone.name} -> {stone.power:.2f} Power | {stone.ghz:.2f} GHz")
            else:
                print("Stone not found.")
        elif command[0].lower() == "combine" and len(command) == 3:
            vs.combine(command[1], command[2])
        elif command[0].lower() == "status":
            vs.status()
        elif command[0].lower() == "history" and len(command) == 2:
            vs.history(command[1])
        elif command[0].lower() == "exit":
            break
        else:
            print("Invalid command.")

        time.sleep(1.5)  # Brief pause before clearing
        cycle += 1

if __name__ == "__main__":
    main()
