import json
from survivor import Survivor

# Load the existing survivors data from JSON file
def load_survivors():
    with open('survivors_data.json', 'r') as f:
        data = json.load(f)
    survivors = [Survivor(**s) for s in data]
    return survivors

all_survivors = load_survivors()

def add_new_survivor(new_survivor):
    # Add the new survivor to the list
    all_survivors.append(new_survivor)

    # Save updated survivors data to JSON file
    with open('survivors_data.json', 'w') as f:
        json.dump([s.__dict__ for s in all_survivors], f, indent=4)
