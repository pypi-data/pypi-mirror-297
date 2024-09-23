import os
import logging
def load_env():
    env_path = os.path.join(os.getcwd(), '.env')
    if os.path.isfile(env_path):
        try:
            with open(env_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        except Exception as e:
            logging.error(f'Error loading .env file: {e}')
            