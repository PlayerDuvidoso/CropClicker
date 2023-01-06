import json
import os

vegetable_ids = ['1', '2', '3', '4', '5']
current_directory = os.getcwd()
basename = fr'assets\images/'

vegetables = {}

for id in vegetable_ids:
    vegetable = input(f'Enter the name for id {id}: ')
    value = input(f'Enter the value of {vegetable}: ')
    price = input(f'Enter the price for {vegetable}: ')

    vegetables[id] = {
        'name': vegetable,
        'value': value,
        'price': price
    }

with open('assets/CropsStorage.json', 'w') as f:
    f.write(json.dumps(vegetables, indent=2))