import json
from game.components import Territory

META_DATA_ROOT_DIRECTORY = './meta_data'
META_DATA_MAP_FILE_PREFIX = '/meta_'
META_DATA_MAP_FILE_POSTFIX = '.json'


def get_map(map_name):
    with open(META_DATA_ROOT_DIRECTORY + META_DATA_MAP_FILE_PREFIX + map_name+META_DATA_MAP_FILE_POSTFIX, 'r') as f:
        map = json.load(f)

    territories_map = {}
    for node, neighbours in map.items():
        territories_map[Territory(node)] = [Territory(x) for x in neighbours]

    return territories_map
