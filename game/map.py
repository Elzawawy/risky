import json
META_DATA_ROOT_DIRECTORY = './meta_data'
META_DATA_MAP_FILE_PREFIX = '/meta_'
META_DATA_MAP_FILE_POSTFIX = '.json'

def get_map(map_name):
    with open(META_DATA_ROOT_DIRECTORY + META_DATA_MAP_FILE_PREFIX + map_name+META_DATA_MAP_FILE_POSTFIX, 'r') as f:
        map = json.load(f)
    return map
