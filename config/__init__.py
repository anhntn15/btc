import json
import os

# general config
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE_PATH = os.path.join(PROJECT_ROOT, 'config', 'config.json')

# data config
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

with open(CONFIG_FILE_PATH, 'r') as f:
    cf = json.load(f)
    API_KEY = cf['api_key']
    API_PREFIX = cf['api_prefix']
    FSYM = cf['fsym']
    TSYM = cf['tsym']

    if API_PREFIX.endswith('/'):  # remove the last `/` if presented
        API_PREFIX = API_PREFIX[:-1]

    print('loaded config from:', CONFIG_FILE_PATH)
