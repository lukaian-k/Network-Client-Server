import json
command = 'freestyle'.upper()

with open('server/database/battle_rap_dictionary.json', 'r') as file:
    info_battle_rap = json.load(file)

    info_battle_rap = {
        key.upper(): value
        for key, value in info_battle_rap.items()
    }

    if command in info_battle_rap:
        print(f'{command}: {info_battle_rap[command]}')