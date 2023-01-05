import json
import os

vegetable_ids = ['1', '2', '3', '4', '5']
current_directory = os.getcwd()
basename = fr'assets\Crops/'

# Initialize an empty dictionary
vegetables = {}

# Iterate over the vegetable names
for id in vegetable_ids:
    # Prompt the user for information about the vegetable
    vegetable = input(f'Enter the name for id {id}: ')
    value = input(f'Enter the value of {vegetable}: ')
    source = input(f'Enter the source for {vegetable}: ')

    # Add an entry for the vegetable to the dictionary
    vegetables[id] = {
        'name': vegetable,
        'value': value
    }

# Print the resulting dictionary
with open('assets/CropsStorage.json', 'w') as f:
    f.write(json.dumps(vegetables, indent=2))