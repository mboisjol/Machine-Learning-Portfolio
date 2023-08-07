import os
import time
import random
import sys

from config.qt_config import QTConfig


def get_abs_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def write_log(msg):
    if not os.path.exists("logs"):
        os.makedirs("logs")
        
    with open(f"logs/{time.time()}.log", "w+") as f:
            f.write(msg)


def get_random_user_agent():
    return USER_AGENTS[int(random.random() * 1000)].strip()


def get_random_user_agent_header():
    return {"User-Agent": get_random_user_agent()}


def append_all_cities():
    cities = []

    with open(_canadian_cities_path, "r") as f:
        lines = f.read().splitlines() 
        cities = lines
    
    return cities


USER_AGENTS = []
RBQ_URLS = []
_canadian_cities_path = ""

if QTConfig.get_config().env == "prod":
    _user_agents_resource_path = get_abs_resource_path("resources/user-agents.txt")
    _rbq_resource_path = get_abs_resource_path("resources/rbq-urls.txt")
    _canadian_cities_path = get_abs_resource_path("resources/canadian-cities.txt")
else:
    _user_agents_resource_path = "resources/user-agents.txt"
    _rbq_resource_path = "resources/rbq-urls.txt"
    _canadian_cities_path = "resources/canadian-cities.txt"

with open(_user_agents_resource_path, "r") as f:
    USER_AGENTS = f.readlines()

with open(_rbq_resource_path, "r") as f:
    RBQ_URLS = f.readlines()
