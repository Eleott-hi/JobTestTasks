import json
import os


config = None

if config is None:
    with open("configs/config.json") as f:
        config = json.load(f)
        config["in_progress"] = False

